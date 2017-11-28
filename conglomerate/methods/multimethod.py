from conglomerate.methods.method import Method, ManyVsManyMethod, OneVsOneMethod, OneVsManyMethod


class MultiMethod(Method):
    MEMBER_ATTRIBUTES = ['_methods']

    def __init__(self, methodCls, querytrackFnList, referencetrackFnList):
        assert any(issubclass(methodCls, superCls)
                   for superCls in [OneVsOneMethod, OneVsManyMethod, ManyVsManyMethod])

        self._methods = []

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
        raise NotImplementedError()

    def setReferenceTrackFileNames(self, trackFnList):
        raise NotImplementedError()

    def setResultFilesDict(self, resultFilesDict):
        raise NotImplementedError()

    def setResultFilesDictList(self, resultFilesDictList):
        assert len(resultFilesDictList) == len(self._methods)
        for i, resultFilesDict in enumerate(resultFilesDictList):
            self._methods[i].setResultFilesDict(resultFilesDict)

    def getResultFilesDict(self):
        raise NotImplementedError()

    def getResultFilesDictList(self):
        return [method.getResultFilesDict() for method in self._methods]

    def _getTool(self):
        raise NotImplementedError()

    def __getattribute__(self, key):
        if key in MultiMethod.__dict__ or key in MultiMethod.MEMBER_ATTRIBUTES:
            return object.__getattribute__(self, key)
        else:
            return CallableAttributeList([object.__getattribute__(self._methods[i], key)
                                          for i in range(len(self._methods))])


class CallableAttributeList(list):
    def __call__(self, *args, **kwArgs):
        retList = [attr.__call__(*args, **kwArgs) for attr in self]
        if retList[0] is None:
            assert all([ret is None for ret in retList])
        elif isinstance(retList[0], dict):
            retDict = {}
            for ret in retList:
                retDict.update(ret)
            return retDict
        elif isinstance([retList[0]], list):
            return [el for subList in retList for el in subList]  # flattens two-level list
        else:
            return retList
