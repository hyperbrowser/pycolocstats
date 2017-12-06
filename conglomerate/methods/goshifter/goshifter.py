from __future__ import absolute_import, division, print_function, unicode_literals

from conglomerate.methods.method import OneVsOneMethod
from conglomerate.tools.constants import GOSHIFTER_TOOL_NAME

__metaclass__ = type


class GoShifter(OneVsOneMethod):
    def _getToolName(self):
        return GOSHIFTER_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setGenomeName(self, genomeName):
        pass

    def setChromLenFileName(self, chromLenFileName):
        pass

    def _setQueryTrackFileName(self, trackFn):
        pass

    def _setReferenceTrackFileName(self, trackFn):
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
