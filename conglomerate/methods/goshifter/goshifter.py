from conglomerate.methods.method import Method
from conglomerate.tools.constants import GOSHIFTER_TOOL_NAME


class GoShifter(Method):
    def _getToolName(self):
        return GOSHIFTER_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setTrackFileNames(self, trackFnList):
        assert len(trackFnList) == 2
        pass

    def setChromLenFileName(self, chromLenFileName):
        pass

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is True

    def _parseResultFiles(self):
        pass

    def getPValue(self):
        pass

    def getTestStatistic(self):
        pass

    def getFullResults(self):
        pass
