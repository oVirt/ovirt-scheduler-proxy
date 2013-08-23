import os
import utils
import sys


def analyze(path, name):
    retValue = (name,)
    try:
        os.chdir(path)
        mod = __import__(name)

        retValue += \
            getAttributes(mod,
                          utils.FILTER,
                          utils.FILTER_REGEX)
        retValue += \
            getAttributes(mod,
                          utils.SCORE,
                          utils.SCORE_REGEX)
        retValue += \
            getAttributes(mod,
                          utils.BALANCE,
                          utils.BALANCE_REGEX)
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
