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
