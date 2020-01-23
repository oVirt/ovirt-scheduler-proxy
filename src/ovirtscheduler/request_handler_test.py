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
import unittest

from request_handler import RequestHandler


class ExecutorTest(unittest.TestCase):

    def setUp(self):
        self.plugin_path = os.environ.get("OSCHEDPROXY_PLUGINS",
                                          os.path.join(os.getcwd(), 'plugins'))

    def test_discover(self):
        executor = RequestHandler(self.plugin_path,
                                  os.path.join(os.getcwd(), 'src',
                                               'ovirtscheduler'))
        ret = executor.discover()
        print(ret)
        assert ret == {
            'balance': {
                'test_plugin': (
                    'This is a fake balance function that always'
                    ' return the guid'
                    ' 33333333-3333-3333-3333-333333333333', '')},
            'filters': {
                'test_plugin': (
                    'This is a simple filter that returns'
                    ' all given host ID', ''),
                'test_failing_plugin': ('This filter is expected to fail and'
                                        ' should be used only in tests.', '')},
            'scores': {
                'test_plugin': (
                    'This is a simple score function that'
                    ' returns all given host ID with score'
                    ' 50', ''),
                'test_failing_plugin': (
                    'This function is expected to fail and'
                    ' should be used only in tests.', '')}}
        pass

    def test_aggregate_filter_results_empty(self):
        """
        Tests if the empty filterRunners array results in None.
        """
        executor = RequestHandler(self.plugin_path,
                                  os.path.join(os.getcwd(), 'src'))
        filterRunners = []
        assert executor.aggregate_filter_results(filterRunners, '') is None

    def test_aggregate_filter_results_singleNone(self):
        """
        Checks that the aggregate filter will return None when
        all runners fail.
        """
        executor = RequestHandler(self.plugin_path,
                                  os.path.join(os.getcwd(), 'src'))

        class NoneResultRunner:
            def __init__(self):
                self._script = 'test'

            def getResults(self):
                return None

            def getReturnCode(self):
                return 1

            def getErrors(self):
                return None

        filterRunners = [NoneResultRunner()]
        assert executor.aggregate_filter_results(filterRunners, '') is None
