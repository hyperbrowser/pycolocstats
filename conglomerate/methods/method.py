from abc import ABCMeta, abstractmethod

from conglomerate.methods.interface import UniformInterface
from conglomerate.methods.typecheck import takes
from conglomerate.tools.exceptions import MissingMandatoryParameters
from conglomerate.tools.job import Job
from conglomerate.tools.tool import Tool


class Method(UniformInterface):
    def __init__(self):
        self._params = self._getTool().createJobParamsDict()
        self._setDefaultParamValues()
        self._resultFilesDict = None

    def _getTool(self):
        return Tool(self._getToolName())

    def setManualParam(self, key, val):
        """
        For setting tool parameters directly, without going through properties (like allowOverlaps)
        """
        self._params[key] = val

    def createJobs(self):
        absentMandatoryParameters = self._params.getAbsentMandatoryParameters()
        if absentMandatoryParameters:
            raise MissingMandatoryParameters(absentMandatoryParameters)
        return [Job(self._getTool(), self._params)]

    def setResultFilesDict(self, resultFilesDict):
        self._resultFilesDict = resultFilesDict
        self._parseResultFiles()

    def getResultFilesDict(self):
        return self._resultFilesDict


class SingleQueryTrackMethodMixin(object):
    __metaclass__ = ABCMeta

    def setQueryTrackFileNames(self, trackFnList):
        assert len(trackFnList) == 1
        self._setQueryTrackFileName(trackFnList[0])

    @abstractmethod
    def _setQueryTrackFileName(self, trackFn):
        pass


class SingleReferenceTrackMethodMixin(object):
    __metaclass__ = ABCMeta

    def setReferenceTrackFileNames(self, trackFnList):
        assert len(trackFnList) == 1
        self._setReferenceTrackFileName(trackFnList[0])

    @abstractmethod
    def _setReferenceTrackFileName(self, trackFn):
        pass


class MultipleQueryTracksMethodMixin(object):
    __metaclass__ = ABCMeta

    def setQueryTrackFileNames(self, trackFnList):
        assert len(trackFnList) > 0
        self._setQueryTrackFileNames(trackFnList)

    @abstractmethod
    def _setQueryTrackFileNames(self, trackFnList):
        pass


class MultipleReferenceTracksMethodMixin(object):
    __metaclass__ = ABCMeta

    def setReferenceTrackFileNames(self, trackFnList):
        assert len(trackFnList) > 0
        self._setReferenceTrackFileNames(trackFnList)

    @abstractmethod
    def _setReferenceTrackFileNames(self, trackFnList):
        pass


class CollectionReferenceTracksMethodMixin(object):
    __metaclass__ = ABCMeta

    def setReferenceTrackFileNames(self, trackFnList):
        assert len(trackFnList) == 0

    @takes(str, str)
    def setPredefinedTrackIndexAndCollection(self, trackIndex, trackCollection):
        self._setPredefinedTrackIndexAndCollection(trackIndex, trackCollection)

    @abstractmethod
    def _setPredefinedTrackIndexAndCollection(self, trackIndex, trackCollection):
        pass


class OneVsOneMethod(SingleQueryTrackMethodMixin,
                     SingleReferenceTrackMethodMixin,
                     Method):
    __metaclass__ = ABCMeta


class OneVsManyMethod(SingleQueryTrackMethodMixin,
                      MultipleReferenceTracksMethodMixin,
                      Method):
    __metaclass__ = ABCMeta


class ManyVsManyMethod(MultipleQueryTracksMethodMixin,
                       MultipleReferenceTracksMethodMixin,
                       Method):
    __metaclass__ = ABCMeta


class OneVsCollectionMethod(SingleQueryTrackMethodMixin,
                            CollectionReferenceTracksMethodMixin,
                            Method):
    __metaclass__ = ABCMeta


class ManyVsCollectionsMethod(MultipleQueryTracksMethodMixin,
                              CollectionReferenceTracksMethodMixin,
                              Method):
    __metaclass__ = ABCMeta
