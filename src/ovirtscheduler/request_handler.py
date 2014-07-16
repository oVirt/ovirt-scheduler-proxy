#
# Copyright 2013 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
from runner import PythonMethodRunner
import utils
import logging
import uuid
from result import Result


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

        resultSet = None
        for runner in filterRunners:

            # if the filter fails, ignore it and continue
            # as if it was not there
            if runner.getReturnCode() or runner.getErrors():
                self._logger.warn('Error in %s (errno: %d, errors: %s)',
                                  runner._script, runner.getReturnCode(),
                                  runner.getErrors())
                continue

            # If there is no result, skip this filter
            if runner.getResults() is None:
                log_adapter.warning('No results from %s' % runner._script)
                continue

            hosts = set(runner.getResults())
            if resultSet is None:
                resultSet = hosts
            else:
                resultSet = resultSet.intersection(hosts)

        if resultSet is not None:
            resultSet = list(resultSet)

        return resultSet

    def run_filters(self, filters, hostIDs, vmID, properties_map):
        result = Result()
        request_id = str(uuid.uuid1())
        log_adapter = \
            utils.RequestAdapter(self._logger,
                                 {'method': 'run_filters',
                                            'request_id': request_id})

        # run each filter in a process for robustness
        log_adapter.info("got request: %s" % str(filters))
        avail_f, missing_f = utils.partition(filters,
                                             lambda f: f in self._filters)

        # handle missing filters
        for f in missing_f:
            log_adapter.warning("Filter requested but was not found: %s" % f)
            result.pluginError(f, "plugin not found: '%s'" % f)

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
        # TODO add timeout config
        if utils.waitOnGroup(filterRunners):
            log_adapter.warning("Waiting on filters timed out")

        log_adapter.debug("Aggregating results")
        filters_results = self.aggregate_filter_results(filterRunners,
                                                        request_id)
        if filters_results is None:
            log_adapter.info('All filters failed, return the full list')
            result.error("all filters failed")
            filters_results = hostIDs

        result.add(filters_results)
        log_adapter.info('returning: %s' % str(filters_results))

        return result

    # accumalate the results
    def aggregate_score_results(self, scoreRunners, request_id):
        log_adapter = \
            utils.RequestAdapter(self._logger,
                                 {'method': 'aggregate_score_results',
                                            'request_id': request_id})

        results = {}
        for runner, weight in scoreRunners:
            # if the scoring function fails, ignore the result
            if runner.getReturnCode() != 0 or runner.getErrors():
                self._logger.warn('Error in %s (errno: %d, errors: %s)',
                                  runner._script, runner.getReturnCode(),
                                  runner.getErrors())
                continue

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
        result = Result()
        request_id = str(uuid.uuid1())
        log_adapter = \
            utils.RequestAdapter(self._logger,
                                 {'method': 'run_cost_functions',
                                            'request_id': request_id})

        # run each filter in a process for robustness
        log_adapter.info("got request: %s" % str(cost_functions))

        # Get the list of known and unknown score functions
        available_cost_f, missing_cost_f = \
            utils.partition(cost_functions, lambda (n, w): n in self._scores)

        # Report the unknown functions
        for name, weight in missing_cost_f:
                log_adapter.warning("requested but was not found: %s" % name)
                result.pluginError(name, "plugin not found: '%s'" % name)

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
            result.error("Waiting on score functions timed out")

        log_adapter.debug("Aggregating results")
        results = self.aggregate_score_results(scoreRunners, request_id)
        result.add(results)
        log_adapter.info('returning: %s' % str(results))
        return result

    def run_load_balancing(self, balance, hostIDs, properties_map):
        result = Result()
        request_id = str(uuid.uuid1())
        log_adapter = \
            utils.RequestAdapter(self._logger,
                                 {'method': 'run_load_balancing',
                                            'request_id': request_id})

        log_adapter.info("got request: %s" % balance)

        if balance not in self._balancers:
            warn_message = "Load balance requested but was not found: %s"\
                           % balance
            log_adapter.warning(warn_message)
            result.pluginError(balance, warn_message)
            return result

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

        if runner.getResults() is None:
            result.add(['', []])
        else:
            result.add(runner.getResults())

        return result
