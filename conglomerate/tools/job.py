import cwltool
import os
import urllib


class JobParamsDict(dict):
    # TODO: Add explicit support for mandatory/optional params?
    def __init__(self, paramDefDict):
        super(JobParamsDict, self).__init__(self)
        self._paramDefDict = paramDefDict

    def __setitem__(self, key, val):
        assert key in self.getAllowedKeys(), \
            '"{}" not in allowed keys: {}'.format(key, ', '.join(self.getAllowedKeys()))

        allowedType = self.getType(key)
        if allowedType == PathStr:
            val = self._assert_and_format_path_type(val)
        else:
            assert isinstance(val, allowedType), \
                '"{}" not of correct type: {}'.format(val, allowedType)
        super(JobParamsDict, self).__setitem__(key, val)

    def _assert_and_format_path_type(self, val):
        assert isinstance(val, str), \
            '"{}" not of correct type: {}'.format(val, str)
        assert os.path.exists(val), \
            'File "{}" does not exist'.format(val)

        topDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..')
        topDirRelPath = os.path.relpath(os.path.abspath(val), topDir)

        return {'class': 'File', 'location': topDirRelPath}

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
    def __init__(self, tool, params):
        self._tool = tool
        self._params = params

    def run(self):
        try:
            cwlTool = self._tool.getCwlTool()
            toolResults = cwlTool(**self._params)
            return self._createResultFilesDict(toolResults)
        except cwltool.factory.WorkflowStatus as ws:
            return self._createResultFilesDict(ws.out)

    @staticmethod
    def _createResultFilesDict(toolResults):
        resultFilesDict = {}
        assert isinstance(toolResults, dict)
        for key, fileinfo in toolResults.items():
            assert isinstance(fileinfo, dict)
            parsedLocation = urllib.parse.urlparse(fileinfo['location'])
            assert parsedLocation.scheme == 'file'
            resultFilesDict[key] = parsedLocation.path
        return resultFilesDict


class PathStr(str):
    pass
