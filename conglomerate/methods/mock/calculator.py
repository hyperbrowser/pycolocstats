from conglomerate.methods.method import Method
from conglomerate.tools.tool import CALCULATOR_TOOL_NAME


class Calculator(Method):
    def _getToolName(self):
        return CALCULATOR_TOOL_NAME

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


class Adder(Calculator):
    def _setDefaultParamValues(self):
        self._params['operation'] = 'add'


class Subtractor(Calculator):
    def _setDefaultParamValues(self):
        self._params['operation'] = 'subtract'
