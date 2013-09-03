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
import utils
import logging


class PythonMethodRunner(Thread):
    def __init__(self, path, module, cls, method, args, request_id=''):
        super(PythonMethodRunner, self).__init__(group=None)
        logger = logging.getLogger()
        self._log_adapter = utils.RequestAdapter(
            logger,
            {'method': 'PythonMethodRunner',
                'request_id': request_id})
        self._path = path
        self._result = None
        self._error = None
        self._process = None
        self._script = self.createScript(module, cls, method, args)
        self.request_id = request_id

    def run(self):
        try:
            self._log_adapter.debug(
                'running %s in %s' % (self._script, self._path))
            self._process = utils.createProcess(self._script, self._path)
            (result, error) = self._process.communicate()
            try:
                self._result = literal_eval(result)
            except Exception as ex:
                if not error:
                    self._error = "Unable to parse result: %s" \
                                  " got error : %s " % (result, ex)
            if error:
                self._error = error
        except Exception as ex:
            self._error = ex

        if(self._error):
            self._log_adapter.error("script %s got error %s" %
                                    (self._script, self._error))

    def getResults(self):
        return self._result

    def getErrors(self):
        return self._error

    def stop(self):
        return utils.killProcess(self._process)

    def createScript(self, module, cls, method, args):
        commandTemplate = \
            "import %(module)s; %(module)s.%(class)s().%(method)s%(args)s"
        commandString = commandTemplate % {
            "module": module,
            "class": cls,
            "method": method,
            "args": repr(utils.createFunctionArgs(args))
        }

        return ["python", "-c", commandString]
