from conglomerate.methods.method import OneVsManyMethod
from conglomerate.tools.constants import GIGGLE_TOOL_NAME


class Giggle(OneVsManyMethod):
    def _getToolName(self):
        return GIGGLE_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def _setQueryTrackFileName(self, trackFn):
        self._params['search_q'] = trackFn

    def _setReferenceTrackFileNames(self, trackFnList):
        self._params['index_i'] = trackFnList

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
