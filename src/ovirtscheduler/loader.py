import os
import utils
import sys


_utils = utils.utils()

'''
    Loads a module and checks if it has certain functions
    Will run as a process for safety, so it prints the result to stdout
'''


def analyze(path, name):
    retValue = (name,)
    try:
        os.chdir(path)
        mod = __import__(name)

        retValue += \
            getAttributes(mod,
                          _utils.FILTER,
                          _utils.FILTER_REGEX)
        retValue += \
            getAttributes(mod,
                          _utils.SCORE,
                          _utils.SCORE_REGEX)
        retValue += \
            getAttributes(mod,
                          _utils.BALANCE,
                          _utils.BALANCE_REGEX)
    except Exception as ex:
        print >> sys.stderr, ex

    print retValue


def getAttributes(mod, function_name, regex_name):
    description = ""
    regex_map = ""
    if hasattr(mod, function_name):
            description = getattr(mod, function_name).__doc__
            if hasattr(mod, regex_name):
                regex_map = getattr(mod, regex_name)
            return ((function_name, description, regex_map),)
    else:
        return ()
