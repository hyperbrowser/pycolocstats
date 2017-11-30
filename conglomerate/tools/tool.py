import cwltool.factory
import docker
import pkg_resources
import yaml

from conglomerate.tools.jobparamsdict import JobParamsDict
from conglomerate.tools.types import PathStr, PathStrList


class Tool(object):
    _cwlToolFactory = cwltool.factory.Factory()

    def __init__(self, toolName):
        self._toolName = toolName
        with open(self._getCWLFilePath(), 'r') as stream:
            self._yaml = yaml.load(stream)
        self._cwlTool = None

    def getCwlTool(self):
        if not self._cwlTool:
            docker.from_env().images.pull(name='conglomerate/%s' % self._toolName, tag="latest")
            self._cwlTool = self._cwlToolFactory.make(self._getCWLFilePath())
            self._cwlTool.factory.execkwargs['use_container'] = True
            self._cwlTool.factory.execkwargs['no_read_only'] = True
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
        paramDefDict = dict(
            [(inp, dict(type=self.getPythonType(inputs[inp]['type']),
                        mandatory=self.isMandatoryParameter(inputs[inp]['type'])))
             for inp in inputs])
        return JobParamsDict(paramDefDict)

    @staticmethod
    def getPythonType(cwlType):
        if isinstance(cwlType, dict) or isinstance(cwlType, list):
            return PathStrList
        typeStr = cwlType[:-1] if cwlType.endswith('?') else cwlType
        return {
            'int': int,
            'float': float,
            'string': str,
            'boolean': bool,
            'File': PathStr
        }[typeStr]

    @staticmethod
    def isMandatoryParameter(cwlType):
        if isinstance(cwlType, list):
            return 'null' not in cwlType
        else:
            return True if isinstance(cwlType, dict) else not cwlType.endswith('?')
