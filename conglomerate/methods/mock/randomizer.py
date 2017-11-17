from conglomerate.methods.method import Method
from conglomerate.tools.tool import RANDOMIZER_TOOL_NAME


class Randomizer(Method):
    def _getToolName(self):
        return RANDOMIZER_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setTrackFileNames(self, trackFnList):
        pass

    def setChromLenFileName(self, chromLenFileName):
        self._params['chrlen'] = chromLenFileName

    def setAllowOverlaps(self, allowOverlaps):
        pass

    def getPValue(self):
        pass

    def getTestStatistic(self):
        pass

    def getFullResults(self):
        pass
