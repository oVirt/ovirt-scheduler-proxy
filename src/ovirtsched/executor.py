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
from runner import ScriptRunner


class PluginExecutor(object):
    '''
    PluginExecutor runs all the plugins in parallel using instances of
    ScriptRunner
    When all threads are joined, the results are aggregated and returned

    Keyword arguments:
    plugin_dir -- the directory where the plugin scripts are located
    '''
    def __init__(self, plugin_dir):
        self._plugin_dir = plugin_dir
        self._filter_dir = os.path.join(self._plugin_dir, 'filters')
        self._cost_dir = os.path.join(self._plugin_dir, '/costs')

    def discover(self):
        # TODO: temporary implementation
        return os.listdir(self._filter_dir)

    def run_filters(self, scriptinput):
        runners = {}
        results = []
        for flter in os.listdir(self._filter_dir):
            runners[flter] = ScriptRunner(flter, scriptinput)
            runners[flter].start()
        for runner in runners.itervalues():
            runner.join()
            runner.get_results()
            #TODO
        return results

    def run_cost_functions(self):
        #TODO
        pass

    def run_loadbalancing(self):
        #TODO
        pass
