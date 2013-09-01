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

FILTER = 'do_filter'
SCORE = 'do_score'
BALANCE = 'do_balance'
REGEX = 'properties_validation'
LOADER_MODULE = 'loader'
LOADER_FUNC = 'analyze'


def createProcess(script, runLocation=None):
    """
        Creates a process from script
    """
    #script should be a list and not a string
    if isinstance(script, basestring):
        script = [script]
    process = subprocess.Popen(script,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=runLocation)
    return process


def execInProcess(script, script_input=None):
    """
       Create a process and execute it
       Done synchronously
    """
    process = createProcess(script)
    return process.communicate(script_input)


def killProcess(process):
    """
    kill only if the process started and has not
    finished yet (returncode is None if the process is alive)
    """
    if (process is not None) and (process.returncode is None):
        return process.kill()


def waitOnGroup(runners, timeout=30):
    """
    wait for a group of runners up to a timeout and stop them
    """
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


def createFunctionArgs(args):
    """
    Converts args to a tuple we can pass to a function using the
    *args method.
    """
    if args is None:
        return tuple()
    if isinstance(args, basestring):
        return (args,)
    # then it must be some kind of list, return as (a,b, ...)
    return tuple(args)


def partition(data, pred):
    """
    Behaves as a simple filter, but returns a tuple with two lists.
    The first one contains elements where the predicate returned True
    and the second one the rest.

    >>> partition([0, 1, 2, 3, 4, 5], lambda x: x % 2)
    ([1, 3, 5], [0, 2, 4])
    """
    # append returns None and we want to return the list, that is why there
    # is the or statement
    return reduce(lambda x, y: x[not pred(y)].append(y) or x, data, ([], []))
