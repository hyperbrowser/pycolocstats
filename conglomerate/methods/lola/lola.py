import math

from conglomerate.methods.interface import RestrictedThroughInclusion
from conglomerate.methods.method import Method
from conglomerate.tools.constants import LOLA_TOOL_NAME


class LOLA(Method):
    def _getToolName(self):
        return LOLA_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def setQueryTrackFileNames(self, trackFnList):
        "For pairwise analysis or one-against-many analysis, this would be a list of one filename"
        assert len(trackFnList) == 1
        self.setManualParam('userset', trackFnList[0])

    def setReferenceTrackFileNames(self, trackFnList):
        "For pairwise analysis, this would be a list of one filename"
        self.setManualParam('regiondb', trackFnList)


    def setChromLenFileName(self, chromLenFileName):
        pass

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is True

    def _parseResultFiles(self):
        #TEMP while missing pandas which chakri really forced to install
        self._pvals = {}
        self._testStats = {}
        return

        import pandas as pd
        resultsFolderPath = self._resultFilesDict['output']
        mainOutput = resultsFolderPath + '/lolaResults/allEnrichments.tsv'
        resultTable = pd.read_table(mainOutput)

        refFns = self._params['regiondb']
        queryFn = self._params['userset']
        refFileIndices = resultTable["dbSet"]

        #Extract pvals
        logPvals = resultTable["pValueLog"]
        pvals = [math.pow(10, float(lp)) for lp in logPvals]
        indicesAndPvalues = zip([refFileIndices, pvals])
        self._pvals = {}
        for index,pval in indicesAndPvalues:
            self._pvals[(queryFn, refFns[index])] = pval

        #Extract test statistic
        testStat = resultTable["logOddsRatio"]
        indicesAndTestStat = zip([refFileIndices, testStat])
        self._testStats = {}
        for index, ts in indicesAndTestStat:
            self._testStats[(queryFn, refFns[index])] = '%.2f'%testStat + ' (logOddsRatio)'

    def getPValue(self):
        return self._pval

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
