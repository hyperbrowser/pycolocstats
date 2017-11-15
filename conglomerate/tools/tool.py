import pkg_resources
import yaml

from conglomerate.tools.job import JobParamsDict


class Tool(object):
    def __init__(self, toolName):
        self._toolName = toolName
        with open(self.getCWLFilePath(), 'r') as stream:
            self._yaml = yaml.load(stream)

    def getDockerImage(self):
        requirements = self._yaml['requirements']
        dockerRequirement = [r for r in requirements if r['class'] == 'DockerRequirement'][0]
        return dockerRequirement['dockerPull']

    def getToolPath(self):
        return pkg_resources.resource_filename('cwl', '%s' % self._toolName)

    def getCWLFilePath(self):
        return pkg_resources.resource_filename('cwl', '%s/tool.cwl' % self._toolName)

    def createJobParamsDict(self):
        inputs = self._yaml['inputs']
        paramDefDict = dict([(inp['id'], self.getPythonType(inp['type'])) for inp in inputs])
        return JobParamsDict(paramDefDict)

    @staticmethod
    def getPythonType(cwlType):
        typeStr = cwlType[:-1] if cwlType.endswith('?') else cwlType
        return {
            'int': int,
            'float': float,
            'string': str,
            'File': dict
        }[typeStr]


CALCULATOR_TOOL = Tool('calculator')
RANDOMIZER_TOOL = Tool('randomizer')
