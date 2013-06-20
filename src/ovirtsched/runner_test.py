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

from runner import ScriptRunner
import os


class RunnerTest(unittest.TestCase):
    def test_with_dummy(self):
        scriptpath = os.path.join(os.getcwd(),
                                  'plugins/filters/dummy.py')
        inputpath = os.path.join(os.getcwd(),
                                 'samples/singlehost.xml')
        runner = ScriptRunner(scriptpath,
                              file(inputpath).read())
        runner.start()
        runner.join()
        result = runner.get_result()
        assert result
        pass
