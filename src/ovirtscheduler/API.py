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


class API(object):
    """
    This class holds the proxy's exposed API to be used by oVirt engine.
    See http://www.ovirt.org/Features/oVirt_External_Scheduling_Proxy
    """

    def __init__(self, executor):
        self._plugin_executor = executor

    def discover(self):
        return self._plugin_executor.discover()

    def runFilters(self, filters, hosts, vm, properties_map):
        return self._plugin_executor.run_filters(
            filters,
            hosts,
            vm,
            properties_map)

    def runCostFunctions(self, cost_functions, hosts, vm, properties_map):
        return self._plugin_executor.run_cost_functions(
            cost_functions,
            hosts,
            vm,
            properties_map)

    def runLoadBalancing(self, balance, hosts, properties_map):
        return self._plugin_executor.run_load_balancing(
            balance,
            hosts,
            properties_map)
