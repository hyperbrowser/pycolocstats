from conglomerate.methods.method import Method
from conglomerate.tools.constants import INTERVALSTATS_TOOL_NAME


class IntervalStats(Method):
    def _getToolName(self):
        return INTERVALSTATS_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setQueryTrackFileNames(self, trackFnList):
        "For pairwise analysis or one-against-many analysis, this would be a list of one filename"
        assert len(trackFnList) == 1
        self._params['q'] = trackFnList[0]

    def setReferenceTrackFileNames(self, trackFnList):
        "For pairwise analysis, this would be a list of one filename"
        assert len(trackFnList) == 1
        self._params['r'] = trackFnList[0]


    def setChromLenFileName(self, chromLenFileName):
        self._params['d'] = chromLenFileName
        # TODO: Add an extra column in between (filled with zeroes), e.g.:
        # chr1	0	249250621
        # chr10	0	135534747
        # chr11	0	135006516
        # ...
        # etc

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
