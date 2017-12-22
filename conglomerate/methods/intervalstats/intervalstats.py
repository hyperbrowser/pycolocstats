from __future__ import absolute_import, division, print_function, unicode_literals

from os import path

from conglomerate.methods.method import OneVsOneMethod
from conglomerate.tools.constants import INTERVALSTATS_TOOL_NAME
from conglomerate.tools.util import getTemporaryFileName

__metaclass__ = type


class IntervalStats(OneVsOneMethod):
    def __init__(self):
        OneVsOneMethod.__init__(self)
        self.setManualParam('o', str('output'))

    def _getToolName(self):
        return INTERVALSTATS_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setGenomeName(self, genomeName):
        pass

    def setChromLenFileName(self, chromLenFileName):
        contents = []
        with open(chromLenFileName, 'r') as f:
            for line in f.readlines():
                newl = line.strip('\n').split('\t')
                contents.append([newl[0], '0', newl[1]])

        tempFileName = getTemporaryFileName()
        sampleFile = open(tempFileName, 'w')
        for c in contents:
            sampleFile.write('\t'.join(c)+'\n')
        sampleFile.flush()

        self._params['d'] = sampleFile.name #chromLenFileName
        # TODO: Add an extra column in between (filled with zeroes), e.g.:
        # chr1	0	249250621
        # chr10	0	135534747
        # chr11	0	135006516
        # ...
        # etc

    def _setQueryTrackFileName(self, trackFn):
        self._params['q'] = trackFn

    def _setReferenceTrackFileName(self, trackFn):
        assert trackFn not in ['prebuilt', 'LOLACore_170206']
        self._params['r'] = trackFn

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is True

    def _parseResultFiles(self):
        # links to output files
        resultsFolderPath = path.join(self._resultFilesDict['output'],'output')

        self._pvals = {}
        self._pvals[(self._params['q'], self._params['r'])] = {}

        self._testStats = {}
        self._testStats[(self._params['q'], self._params['r'])] = {}

        with open(resultsFolderPath, 'r') as f:
            for line in f.readlines():
                newLine = line.strip('\n').split('\t')
                self._pvals[(self._params['q'], self._params['r'])][newLine[0]] = newLine[6]
                self._testStats[(self._params['q'], self._params['r'])][newLine[0]] = newLine[3]

    def _parseIntervalStatsSummaryStat(self,threshold):
        resultsFolderPath = path.join(self._resultFilesDict['output'], 'output')
        mainOutput = resultsFolderPath
        fullTable = [line.split() for line in open(mainOutput)]
        pvals = []
        for row in fullTable:
            pval = row[6]
            pvals.append(float(pval))
        summaryStat = sum(pval <= threshold for pval in pvals) / float(len(pvals))
        return summaryStat

    def getPValue(self):
        #return self._pvals
        return {(self._params['q'], self._params['r']): 'N/A'}

    def getTestStatistic(self):
        #return self._testStats
        return {(self._params['q'], self._params['r']): self._parseIntervalStatsSummaryStat(threshold=0.05)}

    def getFullResults(self):
        resultsFolderPath = path.join(self._resultFilesDict['output'], 'output')
        return {(self._params['q'], self._params['r']): open(resultsFolderPath).read().replace('\n','<br>\n')}

    def preserveClumping(self, preserve):
        # not sure yet
        assert preserve is False

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        pass

    def setColocMeasure(self, colocMeasure):
        pass

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        assert preservationScheme is True

    def getErrorDetails(self):
        assert not self.ranSuccessfully()
        #Not checked if informative
        return open(self._resultFilesDict['stderr']).read()
