from conglomerate.methods.interface import UniformInterface
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

    def createJob(self):
        absentMandatoryParameters = self._params.getAbsentMandatoryParameters()
        if absentMandatoryParameters:
            raise MissingMandatoryParameters(absentMandatoryParameters)
        return Job(self._getTool(), self._params)

    def setResultFilesDict(self, resultFilesDict):
        self._resultFilesDict = resultFilesDict
        self._parseResultFiles()

    def getResultFilesDict(self):
        return self._resultFilesDict
