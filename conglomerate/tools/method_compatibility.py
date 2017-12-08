from itertools import product

from conglomerate.methods.multimethod import MultiMethod


def getCompatibleMethodObjects(selectionsValues, queryTrack, refTracks, methodClasses):
    workingMethodObjects = []
    multiChoiceList = product(*selectionsValues)
    for choiceTupleList in multiChoiceList:
        for methodClass in methodClasses:
            try:
                currMethod = MultiMethod(methodClass, queryTrack, refTracks)
                for methodName, choice in choiceTupleList:
                    if isinstance(choice, list):
                        getattr(currMethod, methodName)(*choice)
                    else:
                        getattr(currMethod, methodName)(choice)
            except Exception as e:
                print(e)
                continue
            workingMethodObjects.append(currMethod)
    return workingMethodObjects

def getCollapsedConfigurationsPerMethod():
    pass