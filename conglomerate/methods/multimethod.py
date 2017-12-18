from __future__ import absolute_import, division, print_function, unicode_literals

from conglomerate.tools.exceptions import AbstractMethodError, ShouldNotOccurError
from conglomerate.methods.method import Method, ManyVsManyMethod, OneVsOneMethod, OneVsManyMethod

__metaclass__ = type


class MultiMethodAbstractMethodsMixin(object):
    def _getToolName(self):
        raise AbstractMethodError()

    def _setDefaultParamValues(self):
        raise AbstractMethodError()

    def setGenomeName(self, genomeName):
        raise AbstractMethodError()

    def setChromLenFileName(self, chromLenFile):
        raise AbstractMethodError()

    def setPredefinedTrackIndexAndCollection(self, trackIndex, trackCollection):
        raise AbstractMethodError()

    def setAllowOverlaps(self, allowOverlaps):
        raise AbstractMethodError()

    def setColocMeasure(self, colocMeasure):
        raise AbstractMethodError()

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        raise AbstractMethodError()

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        raise AbstractMethodError()

    def preserveClumping(self, preserve):
        raise AbstractMethodError()

    def _parseResultFiles(self):
        raise AbstractMethodError()

    def getPValue(self):
        raise AbstractMethodError()

    def getTestStatistic(self):
        raise AbstractMethodError()

    def getFullResults(self):
        raise AbstractMethodError()


class MultiMethod(MultiMethodAbstractMethodsMixin, Method):
    MEMBER_ATTRIBUTES = ['_methods','_methodCls','__repr__','annotatedChoices', 'ranSuccessfully']

    def __init__(self, methodCls, querytrackFnList, referencetrackFnList):
        assert any(issubclass(methodCls, superCls)
                   for superCls in [OneVsOneMethod, OneVsManyMethod, ManyVsManyMethod])

        self._methods = []
        self._methodCls = methodCls

        queryTracksInputs = [querytrackFnList]
        refTrackInputs = [referencetrackFnList]

        if len(querytrackFnList) > 1:
            if any(issubclass(methodCls, superCls)
                   for superCls in [OneVsOneMethod, OneVsManyMethod]):
                queryTracksInputs = [[track] for track in querytrackFnList]

        if len(referencetrackFnList) > 1:
            if issubclass(methodCls, OneVsOneMethod):
                refTrackInputs = [[track] for track in referencetrackFnList]

        for queryTrackInput in queryTracksInputs:
            for refTrackInput in refTrackInputs:
                method = methodCls()
                method.setQueryTrackFileNames(queryTrackInput)
                method.setReferenceTrackFileNames(refTrackInput)
                self._methods.append(method)

    def setQueryTrackFileNames(self, trackFnList):
        raise ShouldNotOccurError()

    def setReferenceTrackFileNames(self, trackFnList):
        raise ShouldNotOccurError()

    def setResultFilesDict(self, resultFilesDict):
        raise ShouldNotOccurError(self._methodCls.__name__)

    def setResultFilesDictList(self, resultFilesDictList):
        assert len(resultFilesDictList) == len(self._methods)
        for i, resultFilesDict in enumerate(resultFilesDictList):
            self._methods[i].setResultFilesDict(resultFilesDict)

    def getResultFilesDict(self):
        raise ShouldNotOccurError()

    def getResultFilesDictList(self):
        return [method.getResultFilesDict() for method in self._methods]

    def _getTool(self):
        raise ShouldNotOccurError()

    def __getattribute__(self, key):
        if key in MultiMethod.__dict__ or key in MultiMethod.MEMBER_ATTRIBUTES:
            return object.__getattribute__(self, key)
        else:
            return CallableAttributeList([object.__getattribute__(self._methods[i], key)
                                          for i in range(len(self._methods))])

    def ranSuccessfully(self):
        statuses = set([m.ranSuccessfully() for m in self._methods])
        assert len(statuses)==1
        return list(statuses)[0]


    def __repr__(self):
        if len(self._methods)>0:
            return "MultiMethod of: " + repr(self._methods[0])
        else:
            return "Empty MultiMethod"

class CallableAttributeList(list):
    def __call__(self, *args, **kwArgs):
        retList = [attr.__call__(*args, **kwArgs) for attr in self]
        if retList[0] is None:
            assert all([ret is None for ret in retList])
        elif isinstance(retList[0], dict):
            retDict = type(retList[0])()
            for ret in retList:
                retDict.update(ret)
            return retDict
        elif isinstance([retList[0]], list):
            return [el for subList in retList for el in subList]  # flattens two-level list
        else:
            return retList
