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
import subprocess
from time import time


class utils(object):
    def __init__(self):
        pass

    FILTER = 'filterFunction'
    FILTER_DESCRIPTION = 'desc_filter'
    FILTER_REGEX = 'regex_filter'
    SCORE = 'scoreFunction'
    SCORE_DESCRIPTION = 'desc_score'
    SCORE_REGEX = 'regex_score'
    BALANCE = 'balanceFunction'
    BALANCE_DESCRIPTION = 'desc_balance'
    BALANCE_REGEX = 'regex_balance'
    LOADER_MODULE = 'loader'
    LOADER_FUNC = 'analyze'

    '''
        Creates a process from script
    '''
    def createProcess(self, script, runLocation):
        #script should be a list and not a string
        if isinstance(script, basestring):
            script = [script]
        process = subprocess.Popen(script,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   cwd=runLocation)
        return process

    '''
       Create a process and execute it
       Done synchronously
    '''
    def execInProcess(self, script, script_input=None):
        process = self.createProcess(script)
        return process.communicate(script_input)

    '''
        kill only if the process started and has not
        finished yet (returncode is None if the process is alive)
    '''
    def killProcess(self, process):
        if (process is not None) and (process.returncode is None):
            return process.kill()

    '''
        wait for a group of runners up to a timeout and stop them
    '''
    def waitOnGroup(self, runners, timeout=30):
        timedOut = False
        expireTime = time() + timeout
        for runner in runners:
            timeLeft = expireTime - time()
            if timeLeft < 0:
                timedOut = True
                break
            runner.join(timeLeft)
        #Make sure we dont have dangling processes
        for runner in runners:
            runner.stop()

        return timedOut

    '''
        converts args to a string
    '''
    def createFunctionStringArgs(self, args):
        if args is None:
            return '()'
        if isinstance(args, basestring):
            return '(' + args + ')'
        # then it must be some kind of list, return as (a,b, ...)
        return str(tuple(args))
