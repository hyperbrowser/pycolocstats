from conglomerate.methods.method import Method
from conglomerate.tools.constants import GENOMETRICORR_TOOL_NAME


class GenometriCorr(Method):
    def _getToolName(self):
        return GENOMETRICORR_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setTrackFileNames(self, trackFnList):
        assert len(trackFnList) == 2
        self._params['query'] = trackFnList[0]
        self._params['reference'] = trackFnList[1]

    def setChromLenFileName(self, chromLenFileName):
        self._params['chromosomes_length'] = chromLenFileName
        # TODO: Replace '\t' with '='

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
