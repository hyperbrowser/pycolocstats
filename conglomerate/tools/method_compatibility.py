import traceback
from itertools import product

from conglomerate.methods.multimethod import MultiMethod
from conglomerate.tools.config import VERBOSE_RUNNING, CATCH_METHOD_EXCEPTIONS


def getCompatibleMethodObjects(selectionsValues, queryTrack, refTracks, methodClasses):
    workingMethodObjects = []
    multiChoiceList = list(product(*selectionsValues))
    for choiceTupleList in multiChoiceList:
        for methodClass in methodClasses:
            try:
                currMethod = None  # In case MultiMethod fails
                currMethod = MultiMethod(methodClass, queryTrack, refTracks)
                currMethod.annotatedChoices = dict(choiceTupleList)
                for methodName, choice in choiceTupleList:
                    if isinstance(choice, list):
                        getattr(currMethod, methodName)(*choice)
                    elif isinstance(choice, dict):
                            getattr(currMethod, methodName)(**choice)
                    else:
                        getattr(currMethod, methodName)(choice)
                currMethod.checkForAbsentMandatoryParameters()
            except:
                if VERBOSE_RUNNING:
                    print('Method not compatible: ', methodClass) #, str(type(e)).replace('<','').replace('>',''), e
                    traceback.print_exc()
                if not CATCH_METHOD_EXCEPTIONS:
                    raise
                continue
            workingMethodObjects.append(currMethod)
    return workingMethodObjects

def getCollapsedConfigurationsPerMethod(workingMethodObjects):
    workingClasses = set([wmo._methodCls for wmo in workingMethodObjects])
    return [wc.__name__ + ' (%i configurations)' % len([wmo for wmo in workingMethodObjects if wmo._methodCls is wc])\
            for wc in workingClasses]
