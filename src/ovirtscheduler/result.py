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

RESULT_OK = 0
RESULT_ERROR = 1
PLUGIN_ERRORS = "plugin_errors"
ERRORS = "errors"


class Result(object):
    def __init__(self):
        self._result = {}
        self._result["result_code"] = RESULT_OK  # no error so far..
        self._result["result"] = []

    def add(self, obj_list):
        self._result["result"].extend(obj_list)

    def pluginError(self, pluginName, errorMsg):
        self._result["result_code"] = RESULT_ERROR
        pluginErrors = self._result.get(PLUGIN_ERRORS, {})
        # get the list of error messages for plugin or a new list
        # if it's the first error
        pluginErrorMessages = pluginErrors.get(pluginName, [])
        pluginErrorMessages.append(errorMsg)
        # put the plugin error list to the error dict
        # we could do that only for the first time,
        # but this way we can save one 'if key in dict'
        pluginErrors[pluginName] = pluginErrorMessages
        self._result[PLUGIN_ERRORS] = pluginErrors

    def error(self, errorMsg):
        self._result["result_code"] = RESULT_ERROR
        errors = self._result.get(ERRORS, [])
        errors.append(errorMsg)
        self._result[ERRORS] = errors

    def to_dict(self):
        return self._result


class FilterResult(Result):
    def __init__(self):
        super(FilterResult, self).__init__()


class WeightResult(Result):
    def __init__(self):
        super(WeightResult, self).__init__()
