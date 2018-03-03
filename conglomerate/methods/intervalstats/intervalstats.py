from __future__ import absolute_import, division, print_function, unicode_literals

from os import path

from conglomerate.methods.interface import RestrictedThroughInclusion
from conglomerate.methods.method import OneVsOneMethod
from conglomerate.core.types import SingleResultValue, TrackFile
from conglomerate.core.constants import INTERVALSTATS_TOOL_NAME
from conglomerate.core.util import getTemporaryFileName
import os

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
        pass
        # if 'd' in self._params:
        #     return
        # contents = []
        # with open(chromLenFileName, 'r') as f:
        #     for line in f.readlines():
        #         newl = line.strip('\n').split('\t')
        #         contents.append([newl[0], '0', newl[1]])
        #
        # tempFileName = getTemporaryFileName()
        # sampleFile = open(tempFileName, 'w')
        # for c in contents:
        #     sampleFile.write('\t'.join(c)+'\n')
        # sampleFile.flush()
        #
        # self._params['d'] = sampleFile.name

    def _setQueryTrackFileName(self, trackFile):
        self._addTrackTitleMapping(os.path.basename(trackFile.path), trackFile.title)
        self._addTrackTitleMapping(trackFile.path, trackFile.title)
        self._params['q'] = trackFile.path

    def _setReferenceTrackFileName(self, trackFile):
        if isinstance(trackFile, TrackFile):
            self._addTrackTitleMapping(os.path.basename(trackFile.path), trackFile.title)
            self._addTrackTitleMapping(trackFile.path, trackFile.title)
            trackFn = trackFile.path
        else:
            trackFn = trackFile
        if trackFn in ['prebuilt', 'LOLACore_170206']:
            self.setNotCompatible()
            return
        self._params['r'] = trackFn

    def setAllowOverlaps(self, allowOverlaps):
        if not allowOverlaps:
            self.setNotCompatible()

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
        return self.getRemappedResultDict({(self._params['q'], self._params['r']): SingleResultValue(None, 'N/A')})

    def getTestStatistic(self):
        #return self._testStats
        testStatVal = self._parseIntervalStatsSummaryStat(threshold=0.05) / 0.05
        testStat = '<span title="' + \
                   self.getTestStatDescr() \
                   + '">' + self._getFormattedVal(testStatVal) + '</span>'
        return self.getRemappedResultDict({(self._params['q'], self._params['r']): SingleResultValue(testStatVal, testStat)})

    @classmethod
    def getTestStatDescr(cls):
        return 'ratio of observed to expected number of proximity p-values below 0.05'

    def getFullResults(self):
        resultsFolderPath = path.join(self._resultFilesDict['output'], 'output')
        return self.getRemappedResultDict({(self._params['q'], self._params['r']): open(resultsFolderPath).read().replace('\n','<br>\n')})

    def preserveClumping(self, preserve):
        # not sure yet
        if preserve:
            self.setNotCompatible()

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        if restrictedAnalysisUniverse is None:
            self.setNotCompatible()
        if not isinstance(restrictedAnalysisUniverse, RestrictedThroughInclusion):
            self.setNotCompatible()
        else:
            self.setManualParam('d', restrictedAnalysisUniverse.trackFile.path)

    def setColocMeasure(self, colocMeasure):
        from conglomerate.methods.interface import ColocMeasureProximity
        if not isinstance(colocMeasure, ColocMeasureProximity):
            self.setNotCompatible()

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        if preservationScheme is not True:
            self.setNotCompatible()

    def getErrorDetails(self):
        assert not self.ranSuccessfully()
        #Not checked if informative
        if self._resultFilesDict is not None and 'stderr' in self._resultFilesDict:
            return open(self._resultFilesDict['stderr']).read().replace('\n','<br>\n')
        else:
            return 'Genometricorr did not provide any error output'
