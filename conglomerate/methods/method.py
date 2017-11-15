from abc import ABCMeta, abstractmethod
import yaml
import cwltool.factory


class Method:
    __metaclass__ = ABCMeta

    PROPERTIES = ["LOGICAL_ARG_1", "LOGICAL_ARG_2", "LOGICAL_ARG_3"]

    cwlToolFactory = cwltool.factory.Factory()

    def run(self, **properties):
        tool = Method.cwlToolFactory.make(self._getToolPath())
        tool.factory.execkwargs["use_container"] = True
        mappedParams = self._mapParams(**properties)
        return tool(**mappedParams)

    def _getToolPath(self):
        return "../../tools/%s/tool.cwl" % self._getToolName()

    def _readInputs(self):
        with open(self._getToolPath(), 'r') as stream:
            try:
                return yaml.load(stream)["inputs"]
            except yaml.YAMLError as exc:
                print(exc)

    def _mapParams(self, **properties):
        inputs = [i["id"] for i in self._readInputs()]
        mappedProperties = {}
        for key, value in self._getMappings().items():
            assert key in Method.PROPERTIES
            assert value in inputs
            mappedProperties[self._getMappings()[key]] = properties[key]
        return mappedProperties

    @abstractmethod
    def _getMappings(self):
        pass

    @abstractmethod
    def _getToolName(self):
        pass
