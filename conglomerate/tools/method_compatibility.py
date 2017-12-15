from itertools import product

from conglomerate.methods.multimethod import MultiMethod


def getCompatibleMethodObjects(selectionsValues, queryTrack, refTracks, methodClasses):
    workingMethodObjects = []
    # print 'TEMP3: ', selectionsValues
    # print 'TEMP4: ', [len(v) for v in selectionsValues]
    multiChoiceList = list(product(*selectionsValues))
    # print 'TEMP2', len(list(multiChoiceList)), len(list(methodClasses))
    for choiceTupleList in multiChoiceList:
        for methodClass in methodClasses:
            try:
                currMethod = MultiMethod(methodClass, queryTrack, refTracks)
                for methodName, choice in choiceTupleList:
                    if isinstance(choice, list):
                        getattr(currMethod, methodName)(*choice)
                    elif isinstance(choice, dict):
                            getattr(currMethod, methodName)(**choice)
                    else:
                        getattr(currMethod, methodName)(choice)
            except Exception, e:
                print str(type(e)).replace('<','').replace('>',''), e
                continue
            workingMethodObjects.append(currMethod)
    return workingMethodObjects

def getCollapsedConfigurationsPerMethod(workingMethodObjects):
    workingClasses = set([wmo._methodCls for wmo in workingMethodObjects])
    return [wc.__name__ + ' (%i configurations)' % len([wmo for wmo in workingMethodObjects if wmo._methodCls is wc])\
            for wc in workingClasses]
