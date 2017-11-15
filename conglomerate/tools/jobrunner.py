import os

import cwltool
import pkg_resources
import yaml


class JobParamsDict(dict):
    def __init__(self, paramDefDict):
        super().__init__(self)
        self._paramDefDict = paramDefDict

    def __setitem__(self, key, val):
        assert key in self._paramDefDict
        assert isinstance(val, self._paramDefDict[key])
        super().__setitem__(key, val)

    def getAllowedKeys(self):
        return self._paramDefDict.keys()

    def getType(self, key):
        return self._paramDefDict[key]


class JobRunner(object):
    @classmethod
    def runJobs(cls, jobs):
        return [job.run() for job in jobs]


class Job(object):
    _cwlToolFactory = cwltool.factory.Factory()

    def __init__(self, tool, params):
        self._tool = tool
        self._params = params

    def run(self):
        tool = self._cwlToolFactory.make(self._tool.getCwlFilePath())
        tool.factory.execkwargs['use_container'] = True
        return tool(**self._params)


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

