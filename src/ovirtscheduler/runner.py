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

    def getReturnCode(self):
        return self._process.returncode

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
