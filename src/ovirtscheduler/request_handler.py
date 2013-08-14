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
from utils import utils
import logging


class RequestHandler(object):
    '''
    RequestHandler runs all the plugins in parallel using instances of
    PythonMethodRunner
    When all threads are joined, the results are aggregated and returned

    Keyword arguments:
    plugin_dir -- the directory where the plugin scripts are located
    '''
    def __init__(self, pluginDir, analyzerDir):
        self._logger = logging.getLogger('RequestHandler')
        self._pluginDir = pluginDir
        self._analyzerDir = analyzerDir
        self._filters = dict()
        self._scores = dict()
        self._balancers = dict()
        self._utils = utils()
        self.loadModules()

    '''
        Safely load the user modules in another process
        and find what they implement
    '''
    def loadModules(self):
        loaderRunners = []
        module_files = []
        for fileName in os.listdir(self._pluginDir):
            if not os.path.splitext(fileName)[1] == '.py':
                continue
            module = os.path.splitext(fileName)[0]
            runner = PythonMethodRunner(
                self._analyzerDir,
                self._utils.LOADER_MODULE,
                self._utils.LOADER_FUNC,
                (self._pluginDir, module))
            loaderRunners.append(runner)
            module_files.append(module)

        logging.info("loadModules::Trying to load the following files: " +
                     str(module_files))
        for runner in loaderRunners:
            runner.start()

        if(self._utils.waitOnGroup(loaderRunners)):
            logging.warning("loadModules::Waiting on loading "
                            "+ modules timed out")

        for runner in loaderRunners:
            logging.debug("loadModules::script: " + str(runner._script))
            logging.info("loadModules::registering: " +
                         str(runner.getResults()))

            if str(runner.getErrors()):
                logging.error("loadModules::External module\
failed with error - %s ", str(runner.getErrors()))

            if runner.getResults() is None:
                continue

            availableFunctions = runner.getResults()
            moduleName = availableFunctions[0]
            for functionName, \
                    description, \
                    custom_properties_map in availableFunctions[1:]:
                if self._utils.FILTER == functionName:
                    self._filters[moduleName]\
                        = (description, custom_properties_map)
                elif self._utils.SCORE == functionName:
                    self._scores[moduleName]\
                        = (description, custom_properties_map)
                elif self._utils.BALANCE == functionName:
                    self._balancers[moduleName]\
                        = (description, custom_properties_map)

        logging.info("loadModules::registering::loaded- " +
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
        filterRunners = []
        logging.info("run_filters:: got filters request: " + str(filters))
        for f in filters:
            if f not in self._filters:
                logging.warning("run_filters::Filter requested but "
                                "+ was not found: " + f)
                continue
            runner = PythonMethodRunner(
                self._pluginDir,
                f,
                self._utils.FILTER,
                (hostIDs, vmID, properties_map))
            filterRunners.append(runner)

        for runner in filterRunners:
            runner.start()

        logging.debug("run_filters::Waiting for filters to finish")
        #TODO add timeout config
        if(self._utils.waitOnGroup(filterRunners)):
            logging.warning("run_filters::Waiting on filters timed out")

        logging.debug("run_filters::Aggregating results")
        return self.aggregate_filter_results(filterRunners)

    def run_cost_functions(self,
                           cost_functions,
                           hostIDs,
                           vmID,
                           properties_map):
        #accumalate the results
        def aggregateResults(scoreRunners):
            results = {}
            for runner, weight in scoreRunners:
                if runner.getResults() is None:
                    continue
                hostScores = runner.getResults()
                for host, score in hostScores:
                    if not host in results:
                        results[host] = 0
                    results[host] += weight * score

            return [(host, totalScore) for host,
                    totalScore in results.iteritems()]

        #run each filter in a process for robustness
        scoreRunners = []
        weights = []
        logging.info("run_cost_functions:: got scoring request: "
                     + str(cost_functions))
        for name, weight in cost_functions:
            if name not in self._scores:
                logging.warning("run_cost_functions::Score function requested"
                                + " but was not found: "
                                + name)
                continue
            runner = PythonMethodRunner(
                self._pluginDir,
                name,
                self._utils.SCORE,
                (hostIDs, vmID, properties_map))
            scoreRunners.append(runner)
            weights.append(weight)

        for runner in scoreRunners:
            runner.start()

        logging.debug("run_cost_functions::Waiting for scoring to finish")
        if(self._utils.waitOnGroup(scoreRunners)):
            logging.warning("run_cost_functions::Waiting on score functions"
                            + " timed out")

        logging.debug("run_cost_functions::Aggregating results")
        return aggregateResults(zip(scoreRunners, weights))

    def run_load_balancing(self, balance, hostIDs, properties_map):
        if balance not in self._balancers:
            logging.warning("run_load_balancing::Load balance requested but "
                            + "was not found: "
                            + balance)
            return

        runner = PythonMethodRunner(self._pluginDir,
                                    balance,
                                    self._utils.BALANCE,
                                    (hostIDs, properties_map))

        runner.start()
        logging.debug("run_load_balancing::Waiting for balance to finish")
        runner.join(30)
        logging.debug("run_load_balancing::returning results")
        return runner.getResults()
