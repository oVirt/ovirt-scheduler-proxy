import os
import utils


_utils = utils.utils()

'''
    Loads a module and checks if it has certain functions
    Will run as a process for safety, so it prints the result to stdout
'''


def analyze(path, name):
    os.chdir(path)
    mod = __import__(name)
    retValue = (name,)
    if hasattr(mod, _utils.FILTER):
        retValue += (_utils.FILTER,)

    if hasattr(mod, _utils.SCORE):
        retValue += (_utils.SCORE,)

    if hasattr(mod, _utils.BALANCE):
        retValue += (_utils.BALANCE,)

    print retValue
