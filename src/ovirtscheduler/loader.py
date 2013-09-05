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
import utils
import sys
import inspect


class loader():
    '''
        Loads a module and checks if it has certain functions
        Will run as a process for safety, so it prints the result to stdout
    '''

    def analyze(self, path, name):
        retValue = (name,)
        try:
            os.chdir(path)
            mod = __import__(name)

            for name, obj in inspect.getmembers(mod, inspect.isclass):
                retValue += \
                    self.getAttributes(obj,
                                       name,
                                       utils.FILTER)
                retValue += \
                    self.getAttributes(obj,
                                       name,
                                       utils.SCORE)
                retValue += \
                    self.getAttributes(obj,
                                       name,
                                       utils.BALANCE)
        except Exception as ex:
            print >> sys.stderr, ex

        print retValue

    def getAttributes(self, cls, cls_name, function_name):
        description = ""
        regex_map = ""
        if hasattr(cls, function_name):
            func = getattr(cls, function_name)
            if func.__doc__:
                description = func.__doc__
            if hasattr(cls, utils.REGEX):
                regex_map = getattr(cls, utils.REGEX)
            return ((cls_name, function_name, description, regex_map),)
        else:
            return ()
