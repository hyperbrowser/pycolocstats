from conglomerate.methods.method import Method
from conglomerate.tools.tool import CALCULATOR_TOOL_NAME


class Calculator(Method):
    def _getToolName(self):
        return CALCULATOR_TOOL_NAME

    def setTrackFileNames(self, trackFnList):
        pass

    def setChromLenFileName(self, chromLenFileName):
        pass

    def setAllowOverlaps(self, allowOverlaps):
        pass

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
