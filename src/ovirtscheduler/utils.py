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


import logging
import subprocess
from functools import reduce
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
    # script should be a list and not a string
    if isinstance(script, str):
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
        runner.join(max(timeLeft, 0.0))

        # check if the join timed out and the thread is still running
        if runner.is_alive():
            timedOut = True
            break

    # Make sure we dont have dangling processes
    for runner in runners:
        runner.stop()

    # Wait for threads to finish and store the return code and error
    for runner in runners:
        runner.join(5.0)

    return timedOut


def createFunctionArgs(args):
    """
    Converts args to a tuple we can pass to a function using the
    *args method.
    """
    if args is None:
        return tuple()
    if isinstance(args, str):
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


class RequestAdapter(logging.LoggerAdapter):
    """
    This example adapter expects the passed in dict-like object to have a
    'connid' key, whose value in brackets is prepended to the log message.
    """
    def process(self, msg, kwargs):
        return '[Request:%s][Method:%s] - %s' % \
               (self.extra['request_id'], self.extra['method'], msg), kwargs
