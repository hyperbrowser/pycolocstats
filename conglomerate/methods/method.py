from abc import ABCMeta, abstractmethod
from conglomerate.tools.job import Job
from conglomerate.tools.tool import Tool


class Method(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._params = self._getTool().createJobParamsDict()
        self._setDefaultParamValues()
        self._resultFilesDict = None

    def _getTool(self):
        return Tool(self._getToolName())

    @abstractmethod
    def _getToolName(self):
        pass

    @abstractmethod
    def _setDefaultParamValues(self):
        pass

    @abstractmethod
    def setTrackFileNames(self, trackFileList):
        pass

    @abstractmethod
    def setChromLenFileName(self, chromLenFile):
        pass

    @abstractmethod
    def setAllowOverlaps(self, allowOverlaps):
        pass

    def setManualParam(self, key, val):
        self._params[key] = val

    def createJob(self):
        return Job(self._getTool(), self._params)

    def setResultFilesDict(self, resultFilesDict):
        self._resultFilesDict = resultFilesDict

    def getResultFilesDict(self):
        return self._resultFilesDict

    @abstractmethod
    def getPValue(self):
        pass

    @abstractmethod
    def getTestStatistic(self):
        pass

    @abstractmethod
    def getFullResults(self):
        pass
