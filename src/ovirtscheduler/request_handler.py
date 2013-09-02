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
import uuid


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
        self._class_to_module_map = {}
        self.loadModules()

    def loadModules(self):
        """
        Safely load the user modules in another process
        and find what they implement
        """
        log_adapter = utils.RequestAdapter(self._logger,
                                           {'method': 'loadModules',
                                            'request_id': 'Main'})
        loaderRunners = []
        module_files = []
        for fileName in os.listdir(self._pluginDir):
            module, ext = os.path.splitext(fileName)
            if not ext == '.py':
                continue
            runner = PythonMethodRunner(
                self._analyzerDir,
                utils.LOADER_MODULE,
                utils.LOADER_MODULE,
                utils.LOADER_FUNC,
                (self._pluginDir, module),
                'Main')
            loaderRunners.append(runner)
            module_files.append(module)

        log_adapter.info("Trying to load the following files: %s" %
                         str(module_files))
        for runner in loaderRunners:
            runner.start()

        if utils.waitOnGroup(loaderRunners):
            log_adapter.warning("Waiting on loading modules timed out")

        for runner in loaderRunners:
            log_adapter.debug("script: %s" % str(runner._script))
            log_adapter.info("registering: %s" % str(runner.getResults()))

            if runner.getErrors():
                log_adapter.error("External module failed with error - %s " %
                                  str(runner.getErrors()))

            if runner.getResults() is None:
                continue

            availableFunctions = runner.getResults()
            moduleName = availableFunctions[0]
            for className, functionName, description, custom_properties_map \
                    in availableFunctions[1:]:
                self._director[functionName][className] = \
                    (description, custom_properties_map)
                self._class_to_module_map[className] = moduleName

        log_adapter.info("registering::loaded- " +
                         "filters:" + str(self._filters) +
                         "    scores:" + str(self._scores) +
                         "    balancers:" + str(self._balancers))

    def discover(self):
        request_id = str(uuid.uuid1())
        log_adapter = utils.RequestAdapter(self._logger,
                                           {'method': 'discover',
                                            'request_id': request_id})

        log_adapter.info('got request')
        log_adapter.info('returning: %s' % str({
            "filters": self._filters,
            "scores": self._scores,
            "balance": self._balancers}))

        return {
            "filters": self._filters,
            "scores": self._scores,
            "balance": self._balancers}

    def aggregate_filter_results(self, filterRunners, request_id):
        log_adapter = \
            utils.RequestAdapter(self._logger,
                                 {'method': 'aggregate_filter_results',
                                            'request_id': request_id})

        resultSet = set()
        for runner in filterRunners:
            if runner.getResults() is None:
                log_adapter.warning('No results from %s' % runner._script)
                continue
            hosts = set(runner.getResults())
            if not resultSet:
                resultSet = set(hosts)
                continue
            resultSet = resultSet.intersection(hosts)
        return list(resultSet)

    def run_filters(self, filters, hostIDs, vmID, properties_map):
        request_id = str(uuid.uuid1())
        log_adapter = \
            utils.RequestAdapter(self._logger,
                                 {'method': 'run_filters',
                                            'request_id': request_id})

        #run each filter in a process for robustness
        log_adapter.info("got request: %s" % str(filters))
        avail_f, missing_f = utils.partition(filters,
                                             lambda f: f in self._filters)

        # handle missing filters
        for f in missing_f:
            log_adapter.warning("Filter requested but was not found: %s" % f)
            raise RuntimeError("plugin not found: " + f)

        # Prepare a generator "list" of runners
        filterRunners = [
            PythonMethodRunner(
                self._pluginDir,
                self._class_to_module_map[f],
                f,
                utils.FILTER,
                (hostIDs, vmID, properties_map),
                request_id)
            for f in avail_f
        ]

        for runner in filterRunners:
            runner.start()

        log_adapter.debug("Waiting for filters to finish")
        #TODO add timeout config
        if utils.waitOnGroup(filterRunners):
            log_adapter.warning("Waiting on filters timed out")

        log_adapter.debug("Aggregating results")
        results = self.aggregate_filter_results(filterRunners, request_id)
        log_adapter.info('returning: %s' % str(results))
        return results

    #accumalate the results
    def aggregate_score_results(self, scoreRunners, request_id):
        log_adapter = \
            utils.RequestAdapter(self._logger,
                                 {'method': 'aggregate_score_results',
                                            'request_id': request_id})

        results = {}
        for runner, weight in scoreRunners:
            hostScores = runner.getResults()
            if hostScores is None:
                log_adapter.warning('No results from %s' % runner._script)
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
        request_id = str(uuid.uuid1())
        log_adapter = \
            utils.RequestAdapter(self._logger,
                                 {'method': 'run_cost_functions',
                                            'request_id': request_id})

        #run each filter in a process for robustness
        log_adapter.info("got request: %s" % str(cost_functions))

        # Get the list of known and unknown score functions
        available_cost_f, missing_cost_f = \
            utils.partition(cost_functions, lambda (n, w): n in self._scores)

        # Report the unknown functions
        for name, weight in missing_cost_f:
                log_adapter.warning("requested but was not found: %s" % name)

        # Prepare a generator "list" with runners and weights
        scoreRunners = [
            (PythonMethodRunner(
                self._pluginDir,
                self._class_to_module_map[name],
                name,
                utils.SCORE,
                (hostIDs, vmID, properties_map),
                request_id), weight)
            for name, weight in available_cost_f
        ]

        for runner, _weight in scoreRunners:
            runner.start()

        log_adapter.debug("Waiting for scoring to finish")
        if utils.waitOnGroup([runner for runner, _weight in scoreRunners]):
            log_adapter.warning("Waiting on score functions timed out")

        log_adapter.debug("Aggregating results")
        results = self.aggregate_score_results(scoreRunners, request_id)
        log_adapter.info('returning: %s' % str(results))
        return results

    def run_load_balancing(self, balance, hostIDs, properties_map):
        request_id = str(uuid.uuid1())
        log_adapter = \
            utils.RequestAdapter(self._logger,
                                 {'method': 'run_load_balancing',
                                            'request_id': request_id})

        log_adapter.info("got request: %s" % balance)

        if balance not in self._balancers:
            log_adapter.warning("Load balance requested but was not found: %s", balance)
            return

        runner = PythonMethodRunner(self._pluginDir,
                                    self._class_to_module_map[balance],
                                    balance,
                                    utils.BALANCE,
                                    (hostIDs, properties_map),
                                    request_id)

        runner.start()
        log_adapter.debug('Waiting for balance to finish')

        runner.join(30)

        log_adapter.info('returning: %s' % str(runner.getResults()))

        return runner.getResults()
