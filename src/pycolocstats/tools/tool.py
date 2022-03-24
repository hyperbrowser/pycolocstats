from __future__ import absolute_import, division, print_function, unicode_literals

import cwltool.factory
import docker
import os
import pkg_resources
import yaml

from cwltool.context import RuntimeContext
from numbers import Number
from pycolocstats.core.config import DEFAULT_JOB_OUTPUT_DIR, TMP_DIR, PULL_DOCKER_IMAGES, \
    USE_TEST_DOCKER_IMAGES
from pycolocstats.core.constants import TEST_TOOL_SUFFIX
from pycolocstats.core.types import PathStr, PathStrList
from pycolocstats.core.util import ensureDirExists
from pycolocstats.tools.jobparamsdict import JobParamsDict

__metaclass__ = type


def memoize(func):
    import functools

    cache = func.cache = {}

    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return memoized_func


class Memoize(type):
    @memoize
    def __call__(cls, *args, **kwargs):
        return super(Memoize, cls).__call__(*args, **kwargs)


class ToolConfig(object):
    __metaclass__ = Memoize

    def __init__(self, toolName):
        self.toolName = toolName

        if USE_TEST_DOCKER_IMAGES:
            oldToolName = self.toolName
            self.toolName += TEST_TOOL_SUFFIX
            if not os.path.exists(self.getCWLFilePath()):
                self.toolName = oldToolName

        with open(self.getCWLFilePath(), 'r') as stream:
            self._yaml = yaml.load(stream, Loader=yaml.Loader)

    def getToolImageName(self):
        return 'colocstats/%s' % self.toolName

    def getDockerImagePullInfo(self):
        requirements = self._yaml['requirements']
        dockerRequirement = [r for r in requirements if r['class'] == 'DockerRequirement'][0]
        return dockerRequirement['dockerPull']

    def getCWLFilePath(self):
        return pkg_resources.resource_filename('pycolocstats',
                                               'cwl/{}/tool.cwl'.format(self.toolName))
    def createJobParamsDict(self):
        inputs = self._yaml['inputs']
        paramDefDict = dict(
            [(inp, dict(type=self._getPythonType(inputs[inp]['type']),
                        mandatory=self._isMandatoryParameter(inputs[inp]['type'])))
             for inp in inputs])
        return JobParamsDict(paramDefDict)

    @staticmethod
    def _getPythonType(cwlType):
        if isinstance(cwlType, dict) or isinstance(cwlType, list):
            return PathStrList
        typeStr = cwlType[:-1] if cwlType.endswith('?') else cwlType
        return {
            'int': int,
            'float': float,
            'long': Number,
            'string': str,
            'boolean': bool,
            'File': PathStr
        }[typeStr]

    @staticmethod
    def _isMandatoryParameter(cwlType):
        if isinstance(cwlType, list):
            return 'null' not in cwlType
        else:
            return True if isinstance(cwlType, dict) else not cwlType.endswith('?')


class Tool(object):
    _cwlToolFactory = None

    def __init__(self, toolName):
        if not self._cwlToolFactory:
            self._cwlToolFactory = self._createToolFactory()
        self._config = ToolConfig(toolName)
        self._cwlTool = None

    @staticmethod
    def _createToolFactory():
        runtime_context = RuntimeContext()
        runtime_context.use_container = True
        runtime_context.no_read_only = True
        return cwltool.factory.Factory(runtime_context=runtime_context)

    @property
    def toolName(self):
        return self._config.toolName

    def getCwlTool(self, jobOutputDir=DEFAULT_JOB_OUTPUT_DIR):
        if not self._cwlTool:
            if PULL_DOCKER_IMAGES:
                docker.from_env().images.pull(self._config.getToolImageName(), tag="latest")
            self._cwlTool = self._cwlToolFactory.make(self._config.getCWLFilePath())

            tmpDir = os.path.abspath(TMP_DIR)
            jobOutputDir = os.path.abspath(jobOutputDir)

            ensureDirExists(tmpDir)
            ensureDirExists(jobOutputDir)

            self._cwlTool.factory.runtime_context.tmpdir_prefix = tmpDir
            self._cwlTool.factory.runtime_context.tmp_outdir_prefix = tmpDir
            self._cwlTool.factory.runtime_context.outdir = jobOutputDir

        return self._cwlTool

    def createJobParamsDict(self):
        return self._config.createJobParamsDict()
