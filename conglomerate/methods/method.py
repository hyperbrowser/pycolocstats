from abc import ABCMeta, abstractmethod

from conglomerate.tools.exceptions import MissingMandatoryParameters
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
        """
        :return: Name of the tool as specified as constants in tools/tool.py. Refers to the
         directory name under the 'cwl' directory.
        """
        pass

    @abstractmethod
    def _setDefaultParamValues(self):
        """
        Sets default values for parameters that:
         1) are mandatory, or
         2) where the required default value is different than the default value defined by the
         tool (if the param is not specified).
        """
        pass

    @abstractmethod
    def setTrackFileNames(self, trackFileList):
        pass

    @abstractmethod
    def setChromListFileName(self, chromListFile):
        pass

    @abstractmethod
    def setChromLenFileName(self, chromLenFile):
        pass

    @abstractmethod
    def setAllowOverlaps(self, allowOverlaps):
        pass

    def setManualParam(self, key, val):
        """
        For setting tool parameters directly, without going through properties (like allowOverlaps)
        """
        self._params[key] = val

    def createJob(self):
        absentMandatoryParameters = self._params.getAbsentMandatoryParameters()
        if absentMandatoryParameters:
            raise MissingMandatoryParameters(absentMandatoryParameters)
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
        """
        :return: Full result output as a string
        """
        pass
