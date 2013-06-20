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

import SocketServer
import SimpleXMLRPCServer
import os
from executor import PluginExecutor


class SimpleThreadedXMLRPCServer(SocketServer.ThreadingMixIn,
                                 SimpleXMLRPCServer.SimpleXMLRPCServer):
    pass


class HandlerClass(object):
    '''
    This class does not follow python naming conventions in it method names
    because these method names refer to RPC method names.
    See http://www.ovirt.org/Features/oVirt_External_Scheduling_Proxy
    '''
    _plugin_executor = None

    def __init__(self, executor):
        self._plugin_executor = executor

    def discover(self):
        return self._plugin_executor.discover()

    def runFilters(self):
        return self._plugin_executor.discover()

    def runCostFunctions(self):
        return self._plugin_executor.run_cost_functions()

    def runLoadBalancing(self):
        return self._plugin_executor.run_loadbalancing()

if __name__ == "__main__":
    server = SimpleThreadedXMLRPCServer(("localhost", 18781), allow_none=True)

    executor = PluginExecutor(os.path.join(os.getcwd(), "plugins"))

    server.register_introspection_functions()
    server.register_instance(HandlerClass(executor))

    server.serve_forever()
