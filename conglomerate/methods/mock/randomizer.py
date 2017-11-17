from conglomerate.methods.method import Method
from conglomerate.tools.tool import RANDOMIZER_TOOL_NAME


class Randomizer(Method):
    def _getToolName(self):
        return RANDOMIZER_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setTrackFileNames(self, trackFnList):
        assert len(trackFnList) == 2
        self._params['t1'] = trackFnList[0]
        self._params['t2'] = trackFnList[1]

    def setChromLenFileName(self, chromLenFileName):
        self._params['chrlen'] = chromLenFileName

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is True

    def getPValue(self):
        pass

    def getTestStatistic(self):
        pass

    def getFullResults(self):
        pass
