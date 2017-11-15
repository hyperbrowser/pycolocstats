from abc import ABCMeta, abstractmethod
from conglomerate.tools.job import Job


class Method(object):
    __metaclass__ = ABCMeta

    PROPERTIES = ['LOGICAL_ARG_1', 'LOGICAL_ARG_2', 'LOGICAL_ARG_3']

    def createJob(self, **properties):
        mappedParams = self._mapParams(**properties)
        return Job(self._getTool(), mappedParams)

    def _mapParams(self, **properties):
        params = self._getTool().createJobParamsDict()

        for prop, param in self._getMappings().items():
            params[param] = properties[prop]

        return params

    @abstractmethod
    def _getMappings(self):
        pass

    @abstractmethod
    def _getTool(self):
        pass
