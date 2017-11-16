from abc import ABCMeta, abstractmethod
from conglomerate.tools.job import Job


class Method(object):
    __metaclass__ = ABCMeta

    PROPERTIES = ['TRACK_1', 'TRACK_2', 'LOGICAL_ARG_1', 'LOGICAL_ARG_2', 'LOGICAL_ARG_3']

    def __init__(self, **properties):
        self._params = self._getTool().createJobParamsDict()

        for prop, param in self._getMappings().items():
            self._params[param] = properties[prop]

    def createJob(self):
        return Job(self._getTool(), self._params)

    def setResultFilesDict(self, resultFilesDict):
        self._resultFilesDict = resultFilesDict

    def getResultFilesDict(self):
        return self._resultFilesDict

    @abstractmethod
    def _getMappings(self):
        pass

    @abstractmethod
    def _getTool(self):
        pass
