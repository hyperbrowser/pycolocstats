from __future__ import absolute_import, division, print_function, unicode_literals

import math

from conglomerate.methods.interface import RestrictedThroughInclusion
from conglomerate.methods.method import OneVsManyMethod
from conglomerate.tools.constants import LOLA_TOOL_NAME

__metaclass__ = type


class LOLA(OneVsManyMethod):
    def _getToolName(self):
        return LOLA_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setGenomeName(self, genomeName):
        pass

    def setChromLenFileName(self, chromLenFileName):
        pass

    def _setQueryTrackFileName(self, trackFn):
        self.setManualParam('userset', trackFn)

    def _setReferenceTrackFileNames(self, trackFnList):
        self.setManualParam('regiondb', trackFnList)

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is True

    def _parseResultFiles(self):
        resultsFolderPath = self._resultFilesDict['output']
        mainOutput = resultsFolderPath + '/lolaResults/allEnrichments.tsv'
        # resultTable = pd.read_table(mainOutput)
        fullTable= [line.split() for line in open(mainOutput)]
        header = fullTable[0]
        resultTable = fullTable[1:]

        refFns = self._params['regiondb']
        queryFn = self._params['userset']
        # refFileIndices = resultTable["dbSet"]
        assert header[1] == 'dbSet'
        refFileIndices = [int(row[1]) for row in resultTable]

        #Extract pvals
        # logPvals = resultTable["pValueLog"]
        assert header[3] == "pValueLog"
        logPvals = [float(row[3]) for row in resultTable]

        #NB assuming that LOLA provides minus log10 values..
        pvals = [math.pow(10, -lp) for lp in logPvals]
        indicesAndPvalues = zip(refFileIndices, pvals)
        self._pvals = {}
        for index,pval in indicesAndPvalues:
            self._pvals[(queryFn, refFns[index-1])] = pval

        #Extract test statistic
        # testStat = resultTable["logOddsRatio"]
        assert header[4] == "logOddsRatio"
        testStat = [float(row[4]) for row in resultTable]

        indicesAndTestStat = zip(refFileIndices, testStat)
        self._testStats = {}
        for index, ts in indicesAndTestStat:
            self._testStats[(queryFn, refFns[index-1])] = '%.2f'%ts + ' (logOddsRatio)'

    def getPValue(self):
        return self._pvals

    def getTestStatistic(self):
        return self._testStats

    def getFullResults(self):
        resultsFolderPath = self._resultFilesDict['output']
        mainOutput = resultsFolderPath + '/lolaResults/allEnrichments.tsv'
        return open(mainOutput).read()

    def preserveClumping(self, preserve):
        assert preserve is False

    #@takes("UniformInterface", any([None, RestrictedThroughInclusion]))
    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        assert isinstance(restrictedAnalysisUniverse, RestrictedThroughInclusion)
        self.setManualParam('useruniverse', restrictedAnalysisUniverse.path)

    def setColocMeasure(self, colocMeasure):
        pass

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        pass
