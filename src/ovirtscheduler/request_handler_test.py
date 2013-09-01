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

import unittest

from request_handler import RequestHandler
import os


class ExecutorTest(unittest.TestCase):

    def test_discover(self):
        executor = RequestHandler(os.path.join(os.getcwd(), 'plugins'),
                                  os.path.join(os.getcwd(), 'src',
                                               'ovirtscheduler'))
        ret = executor.discover()
        print ret
        assert ret == {'balance':
                      {'test_plugin':
                       ('This is a fake balance function that always '
                        'return the guid '
                        '33333333-3333-3333-3333-333333333333', '')},
                       'filters':
                       {'test_plugin':
                        ('This is a simple filter that '
                         'returns all given host ID', '')},
                       'scores':
                       {'test_plugin':
                        ('This is a simple score function that returns '
                         'all given host ID with score 50', '')}}
        pass

    def test_aggregate_filter_results_empty(self):
        """
        Tests if the empty filterRunners array results in an None or exception
        in such cases the xmlrpc will fail
        """
        executor = RequestHandler(os.path.join(os.getcwd(), 'plugins'),
                                  os.path.join(os.getcwd(), 'src'))
        filterRunners = []
        assert executor.aggregate_filter_results(filterRunners) is not None

    def test_aggregate_filter_results_singleNone(self):
        """
        Checks that the aggregate filter will not return a None or exception
        even if the runner returns None
        """
        executor = RequestHandler(os.path.join(os.getcwd(), 'plugins'),
                                  os.path.join(os.getcwd(), 'src'))

        class NoneResultRunner:
            def __init__(self):
                self._script = 'test'

            def getResults(self):
                return None

        filterRunners = [NoneResultRunner()]
        assert executor.aggregate_filter_results(filterRunners) is not None
