from __future__ import absolute_import, division, print_function, unicode_literals

from os import path, listdir

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
        textOut = self.getResultFilesDict()['stdout']

        self._pvals={}

        #get p-value from stdout output
        pValText = 'p-value = '
        valStart = textOut.find(pValText)
        valEnd = textOut.find('Detailed')
        self._pvals[(self._params['a'], self._params['o'])] = textOut[valStart + len(pValText):valEnd]
        self._testStats[(self._params['a'], self._params['o'])] = -1

        for fi in listdir(path.join(self._resultFilesDict['output'])):
            if 'nperm10.enrich' in fi:
                with open(path.join(self._resultFilesDict['output'], fi), 'r') as f:
                    self._testStats[(self._params['a'], self._params['o'])] = f.readlines()[1].split('\t')[1]


    def getPValue(self):
        return self._pvals

    def getTestStatistic(self):
        return self._testStats

    def getFullResults(self):
        return open(self.getResultFilesDict()['stdout']).read()

    def preserveClumping(self, preserve):
        pass

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        pass

    def setColocMeasure(self, colocMeasure):
        pass

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        pass
