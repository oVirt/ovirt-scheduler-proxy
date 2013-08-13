import os
import utils


_utils = utils.utils()

'''
    Loads a module and checks if it has certain functions
    Will run as a process for safety, so it prints the result to stdout
'''


def analyze(path, name):
    try:
        os.chdir(path)
        mod = __import__(name)
        retValue = (name,)
        if hasattr(mod, _utils.FILTER):
            if hasattr(mod, _utils.FILTER_DESCRIPTION):
                description, custom_properties_map\
                    = getattr(mod, _utils.FILTER_DESCRIPTION)()
                retValue += ((_utils.FILTER, description, custom_properties_map),)
            else:
                retValue += ((_utils.FILTER, "", ""),)

        if hasattr(mod, _utils.SCORE):
            if hasattr(mod, _utils.SCORE_DESCRIPTION):
                description, custom_properties_map\
                    = getattr(mod, _utils.SCORE_DESCRIPTION)()
                retValue += ((_utils.SCORE, description, custom_properties_map),)
            else:
                retValue += ((_utils.SCORE, "", ""),)

        if hasattr(mod, _utils.BALANCE):
            if hasattr(mod, _utils.BALANCE_DESCRIPTION):
                description, custom_properties_map\
                    = getattr(mod, _utils.BALANCE_DESCRIPTION)()
                retValue += ((_utils.BALANCE, description, custom_properties_map),)
            else:
                retValue += ((_utils.BALANCE, "", ""),)
    except Exception as ex:
        print >> sys.stderr, ex

    print retValue
