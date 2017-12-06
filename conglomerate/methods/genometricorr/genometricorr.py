from __future__ import absolute_import, division, print_function, unicode_literals

from conglomerate.methods.method import OneVsOneMethod
from conglomerate.tools.constants import GENOMETRICORR_TOOL_NAME

__metaclass__ = type


class GenometriCorr(OneVsOneMethod):
    def _getToolName(self):
        return GENOMETRICORR_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setGenomeName(self, genomeName):
        pass

    def setChromLenFileName(self, chromLenFileName):
        self._params['chromosomes_length'] = chromLenFileName
        # TODO: Replace '\t' with '='

    def _setQueryTrackFileName(self, trackFn):
        self._params['query'] = trackFn

    def _setReferenceTrackFileName(self, trackFn):
        self._params['reference'] = trackFn

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
