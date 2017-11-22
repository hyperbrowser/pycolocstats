from conglomerate.methods.method import Method
from conglomerate.tools.constants import STEREOGENE_TOOL_NAME


class StereoGene(Method):
    def _getToolName(self):
        return STEREOGENE_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setTrackFileNames(self, trackFnList):
        self._params['tracks'] = trackFnList

    def setChromLenFileName(self, chromLenFileName):
        self._params['chrom'] = chromLenFileName

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
