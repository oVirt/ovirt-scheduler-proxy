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
from ast import literal_eval
from utils import utils


class PythonMethodRunner(Thread):
    def __init__(self, path, module, method, args):
        super(PythonMethodRunner, self).__init__(group=None)
        self._path = path
        self._result = None
        self._error = None
        self._process = None
        self._utils = utils()
        self._script = self.createScript(module, method, args)

    def run(self):
        try:
            self._process = self._utils.createProcess(self._script, self._path)
            (result, error) = self._process.communicate()
            self._result = literal_eval(result)
            self._error = error
        except Exception as ex:
            self._error = ex

    def getResults(self):
        return self._result

    def getErrors(self):
        return self._error

    def stop(self):
        return self._utils.killProcess(self._process)

    def createScript(self, module, method, args):
        commandString = (
            "import " +
            module + ";" +
            module + "." +
            method + self._utils.createFunctionStringArgs(args))
        return ["python", "-c", commandString]
