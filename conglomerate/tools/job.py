import cwltool
import urllib


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
