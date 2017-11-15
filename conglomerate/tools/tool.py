import pkg_resources
import yaml

from conglomerate.tools.job import JobParamsDict


class Tool(object):
    def __init__(self, toolName):
        self._toolName = toolName

    def getCwlFilePath(self):
        return pkg_resources.resource_filename('cwl', '%s/tool.cwl' % self._toolName)

    def createJobParamsDict(self):
        with open(self.getCwlFilePath(), 'r') as stream:
            inputs = yaml.load(stream)['inputs']
            paramDefDict = dict([(inp['id'], self.getPythonType(inp['type'])) for inp in inputs])
        return JobParamsDict(paramDefDict)

    @staticmethod
    def getPythonType(cwlType):
        typeStr = cwlType[:-1] if cwlType.endswith('?') else cwlType
        return {
            'int': int,
            'float': float,
            'string': str
        }[typeStr]


CALCULATOR_TOOL = Tool('calculator')
RANDOMIZER_TOOL = Tool('randomizer')
