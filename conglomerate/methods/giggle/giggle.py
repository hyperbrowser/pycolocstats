from conglomerate.methods.method import Method
from conglomerate.tools.constants import GIGGLE_TOOL_NAME


class Giggle(Method):
    def _getToolName(self):
        return GIGGLE_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setQueryTrackFileNames(self, trackFnList):
        "For pairwise analysis or one-against-many analysis, this would be a list of one filename"
        self._params['search_q'] = trackFnList[0]

    def setReferenceTrackFileNames(self, trackFnList):
        "For pairwise analysis, this would be a list of one filename"
        self._params['index_i'] = [trackFnList[0], trackFnList[1], trackFnList[2]]

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


    def preserveClumping(self, preserve):
        pass

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        pass

    def setColocMeasure(self, colocMeasure):
        pass

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        pass
