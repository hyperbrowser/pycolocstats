import cwltool.factory
import docker


class JobParamsDict(dict):
    def __init__(self, paramDefDict):
        super(JobParamsDict, self).__init__(self)
        self._paramDefDict = paramDefDict

    def __setitem__(self, key, val):
        assert key in self.getAllowedKeys(), \
            '"{}" not in allowed keys: {}'.format(key, ', '.join(self.getAllowedKeys()))
        assert isinstance(val, self.getType(key)), \
            '"{}" not of correct type: {}'.format(val, self.getType(key))
        super(JobParamsDict, self).__setitem__(key, val)

    def getAllowedKeys(self):
        return self._paramDefDict.keys()

    def getType(self, key):
        return self._paramDefDict[key]

    def __repr__(self):
        retStr = super(JobParamsDict, self).__repr__()
        retStr += '\nAllowed params:\n'
        for key in self.getAllowedKeys():
            retStr += '\t%s: %s\n' % (key, self.getType(key))
        return retStr


class Job(object):
    _cwlToolFactory = cwltool.factory.Factory()

    def __init__(self, tool, params):
        self._tool = tool
        self._params = params

    def run(self):
        path = self._tool.getToolPath()
        docker.from_env().images.build(path=path, tag=self._tool.getDockerImage())
        tool = self._cwlToolFactory.make(self._tool.getCWLFilePath())
        tool.factory.execkwargs['use_container'] = True
        return tool(**self._params)


class JobRunner(object):
    @classmethod
    def runJobs(cls, jobs):
        return [job.run() for job in jobs]
