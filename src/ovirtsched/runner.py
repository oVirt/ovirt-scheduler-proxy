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

from threading import Thread
import subprocess


class ScriptRunner(Thread):
    '''
    This class is responsible for running a single script and returning the
    output of it.
    '''
    def __init__(self, script, script_input=None):
        super(ScriptRunner, self).__init__(group=None, name=script)
        self._script = script
        self._script_input = script_input

    def run(self):
        process = subprocess.Popen([self._script], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE)
        (self._result, _ignore) = process.communicate(self._script_input)
        pass

    def get_result(self):
        return self._result
