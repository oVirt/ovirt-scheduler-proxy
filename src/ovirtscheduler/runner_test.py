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

import unittest

from runner import PythonMethodRunner
import os


class RunnerTest(unittest.TestCase):
    def test_with_dummy(self):
        scriptpath = os.path.join(os.getcwd(),
                                  'plugins')
        runner = PythonMethodRunner(scriptpath,
                                    'test_plugin',
                                    'test_plugin',
                                    'do_filter',
                                    [['11111111-1111-1111-1111-111111111111',
                                      '22222222-2222-2222-2222-222222222222'],
                                     '33333333-3333-3333-3333-333333333333',
                                     ''])
        runner.start()
        runner.join(5)
        result = runner.getResults()
        assert result is not None
        pass
