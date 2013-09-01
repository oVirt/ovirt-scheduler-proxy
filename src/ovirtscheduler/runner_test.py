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
