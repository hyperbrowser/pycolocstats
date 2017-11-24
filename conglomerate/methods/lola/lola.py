from conglomerate.methods.method import Method
from conglomerate.tools.constants import LOLA_TOOL_NAME
import pandas as pd


class LOLA(Method):
    def _getToolName(self):
        return LOLA_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setQueryTrackFileNames(self, trackFnList):
        "For pairwise analysis or one-against-many analysis, this would be a list of one filename"
        assert len(trackFnList) == 1
        pass

    def setReferenceTrackFileNames(self, trackFnList):
        "For pairwise analysis, this would be a list of one filename"
        assert len(trackFnList) == 1
        pass


    def setChromLenFileName(self, chromLenFileName):
        pass

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is True

    def _parseResultFiles(self):


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
