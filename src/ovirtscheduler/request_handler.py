#
# Copyright 2013 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#


import os
from runner import PythonMethodRunner
import utils
import logging


class RequestHandler(object):
    """
    RequestHandler runs all the plugins in parallel using instances of
    PythonMethodRunner
    When all threads are joined, the results are aggregated and returned

    Keyword arguments:
    plugin_dir -- the directory where the plugin scripts are located
    """
    def __init__(self, pluginDir, analyzerDir):
        self._logger = logging.getLogger('RequestHandler')
        self._pluginDir = pluginDir
        self._analyzerDir = analyzerDir
        self._filters = dict()
        self._scores = dict()
        self._balancers = dict()
        self._director = {
            utils.FILTER: self._filters,
            utils.BALANCE: self._balancers,
            utils.SCORE: self._scores
        }
        self.loadModules()

    def loadModules(self):
        """
        Safely load the user modules in another process
        and find what they implement
        """
        loaderRunners = []
        module_files = []
        for fileName in os.listdir(self._pluginDir):
            module, ext = os.path.splitext(fileName)
            if not ext == '.py':
                continue
            runner = PythonMethodRunner(
                self._analyzerDir,
                utils.LOADER_MODULE,
                utils.LOADER_FUNC,
                (self._pluginDir, module))
            loaderRunners.append(runner)
            module_files.append(module)

        self._logger.info("loadModules::Trying to load the following "
                          "files: %s",
                          str(module_files))
        for runner in loaderRunners:
            runner.start()

        if utils.waitOnGroup(loaderRunners):
            self._logger.warning("loadModules::Waiting on loading "
                                 "modules timed out")

        for runner in loaderRunners:
            self._logger.debug("loadModules::script: %s", str(runner._script))
            self._logger.info("loadModules::registering: %s",
                              str(runner.getResults()))

            if str(runner.getErrors()):
                self._logger.error("loadModules::External module "
                                   "failed with error - %s ",
                                   str(runner.getErrors()))

            if runner.getResults() is None:
                continue

            availableFunctions = runner.getResults()
            moduleName = availableFunctions[0]
            for functionName, description, custom_properties_map \
                    in availableFunctions[1:]:
                self._director[functionName][moduleName] = \
                    (description, custom_properties_map)

        self._logger.info("loadModules::registering::loaded- "
                          "filters:" + str(self._filters) +
                          "    scores:" + str(self._scores) +
                          "    balancers:" + str(self._balancers))

    def discover(self):
        #temporary?
        return {
            "filters": self._filters,
            "scores": self._scores,
            "balance": self._balancers}

    def aggregate_filter_results(self, filterRunners):
        resultSet = set()
        for runner in filterRunners:
            if runner.getResults() is None:
                self._logger.warn('No results from %s', runner._script)
                continue
            hosts = set(runner.getResults())
            if not resultSet:
                resultSet = set(hosts)
                continue
            resultSet = resultSet.intersection(hosts)
        return list(resultSet)

    def run_filters(self, filters, hostIDs, vmID, properties_map):
        #Intersects the results from the filters
        #run each filter in a process for robustness
        self._logger.info("run_filters:: got filters request: %s",
                          str(filters))
        avail_f, missing_f = utils.partition(filters,
                                             lambda f: f in self._filters)

        # report missing filters
        for f in missing_f:
            self._logger.warning("run_filters::Filter requested but "
                                 "was not found: %s", f)

        # Prepare a generator "list" of runners
        filterRunners = [
            PythonMethodRunner(
                self._pluginDir,
                f,
                utils.FILTER,
                (hostIDs, vmID, properties_map))
            for f in avail_f
        ]

        for runner in filterRunners:
            runner.start()

        self._logger.debug("run_filters::Waiting for filters to finish")
        #TODO add timeout config
        if utils.waitOnGroup(filterRunners):
            self._logger.warning("run_filters::Waiting on filters timed out")

        self._logger.debug("run_filters::Aggregating results")
        return self.aggregate_filter_results(filterRunners)

    #accumalate the results
    def aggregate_score_results(self, scoreRunners):
        results = {}
        for runner, weight in scoreRunners:
            hostScores = runner.getResults()
            if hostScores is None:
                continue
            for host, score in hostScores:
                results.setdefault(host, 0)
                results[host] += weight * score

        return list(results.items())

    def run_cost_functions(self,
                           cost_functions,
                           hostIDs,
                           vmID,
                           properties_map):
        #run each filter in a process for robustness
        self._logger.info("run_cost_functions:: got scoring request: %s",
                          str(cost_functions))

        # Get the list of known and unknown score functions
        available_cost_f, missing_cost_f = \
            utils.partition(cost_functions, lambda (n, w): n in self._scores)

        # Report the unknown functions
        for name, weight in missing_cost_f:
                self._logger.warning("run_cost_functions::Score function"
                                     " requested but was not found: %s", name)

        # Prepare a generator "list" with runners and weights
        scoreRunners = [
            (PythonMethodRunner(
                self._pluginDir,
                name,
                utils.SCORE,
                (hostIDs, vmID, properties_map)), weight)
            for name, weight in available_cost_f
        ]

        for runner, _weight in scoreRunners:
            runner.start()

        self._logger.debug("run_cost_functions::Waiting for scoring to finish")
        if utils.waitOnGroup([runner for runner, _weight in scoreRunners]):
            self._logger.warning("run_cost_functions::Waiting on score"
                                 " functions timed out")

        self._logger.debug("run_cost_functions::Aggregating results")
        return self.aggregate_score_results(scoreRunners)

    def run_load_balancing(self, balance, hostIDs, properties_map):
        if balance not in self._balancers:
            self._logger.warning("run_load_balancing::Load balance requested"
                                 " but was not found: %s", balance)
            return

        runner = PythonMethodRunner(self._pluginDir,
                                    balance,
                                    utils.BALANCE,
                                    (hostIDs, properties_map))

        runner.start()
        self._logger.debug("run_load_balancing::Waiting for balance to finish")
        runner.join(30)
        self._logger.debug("run_load_balancing::returning results")
        return runner.getResults()
