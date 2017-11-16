import cwltool.factory
import docker
import pkg_resources
import yaml

from conglomerate.tools.job import JobParamsDict, PathStr


class Tool(object):
    _cwlToolFactory = cwltool.factory.Factory()

    def __init__(self, toolName):
        self._toolName = toolName
        with open(self._getCWLFilePath(), 'r') as stream:
            self._yaml = yaml.load(stream)
        self._cwlTool = None

    def getCwlTool(self):
        if not self._cwlTool:
            path = self._getToolPath()
            docker.from_env().images.build(path=path, tag=self._getDockerImagePullInfo())
            self._cwlTool = self._cwlToolFactory.make(self._getCWLFilePath())
            self._cwlTool.factory.execkwargs['use_container'] = True
        return self._cwlTool

    def _getDockerImagePullInfo(self):
        requirements = self._yaml['requirements']
        dockerRequirement = [r for r in requirements if r['class'] == 'DockerRequirement'][0]
        return dockerRequirement['dockerPull']

    def _getToolPath(self):
        return pkg_resources.resource_filename('cwl', '%s' % self._toolName)

    def _getCWLFilePath(self):
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
            'File': PathStr
        }[typeStr]


CALCULATOR_TOOL = Tool('calculator')
RANDOMIZER_TOOL = Tool('randomizer')
GENOMETRICORR_TOOL = Tool('genometricorr')
