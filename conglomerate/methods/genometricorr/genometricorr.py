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
        self._results = self._parseGenometricorrStdout(outputPath=self._resultFilesDict['stdout'])
        print(self._results)

    def _parseGenometricorrStdout(self, outputPath):
        from collections import defaultdict
        stdoutFile = outputPath
        data = defaultdict(dict)
        for line in open(stdoutFile):
            cols = line.strip().split()
            if len(cols) == 2:
                regionNames = cols
            elif len(cols) == 3:
                data[cols[0]][regionNames[0]] = cols[1]
                data[cols[0]][regionNames[1]] = cols[2]
            # else:
            #     raise AssertionError('Number of fields are not either two or three')
        return data

    def getPValue(self):
        print(self._results['jaccard.measure.p.value']['awhole'])

    def getTestStatistic(self):
        print(self._results['jaccard.measure']['awhole'])

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
