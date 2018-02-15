from __future__ import absolute_import, division, print_function, unicode_literals

import math
from collections import OrderedDict

from conglomerate.methods.interface import RestrictedThroughInclusion, ColocMeasureOverlap
from conglomerate.methods.method import OneVsManyMethod
from conglomerate.core.types import SingleResultValue
from conglomerate.core.constants import LOLA_TOOL_NAME

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

    def _setQueryTrackFileName(self, trackFile):
        self._addTrackTitleMapping(trackFile.path, trackFile.title)
        self.setManualParam('userset', trackFile.path)

    def _setReferenceTrackFileNames(self, trackFileList):
        if trackFileList == ['prebuilt','LOLACore_170206']:
            self.setManualParam('trackIndex', str('LOLACore_170206'))
            self.setManualParam('trackCollection', str('codex'))
            self.setManualParam('genome', str('hg19'))
        else:
            trackFnList = []
            for trackFile in trackFileList:
                self._addTrackTitleMapping(trackFile.path, trackFile.title)
                trackFnList.append(trackFile.path)
            self.setManualParam('regiondb', trackFnList)

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is True

    def _parseResultFiles(self):
        resultsFolderPath = self._resultFilesDict['output']
        mainOutput = resultsFolderPath + '/lolaResults/allEnrichments.tsv'
        #Probably not needed, as will otherwise raise exception..
        #import os.path
        # if not os.path.exists(mainOutput):
        #     self._ranSuccessfully = False
        #     return
        # resultTable = pd.read_table(mainOutput)
        fullTable= [line.split('\t') for line in open(mainOutput)]
        header = fullTable[0]
        resultTable = fullTable[1:]

        if 'regiondb' in self._params:
            refFns = self._params['regiondb']
        else:
            refFns = [line.split('\t')[14] for line in open(mainOutput).readlines()[1:]]
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
            self._testStats[(queryFn, refFns[index-1])] = \
                SingleResultValue(ts, '<span title="' + \
                                  self.getTestStatDescr() \
                                  + '">' + '%.1f'%ts + '</span>')

        self._ranSuccessfully = True

    @classmethod
    def getTestStatDescr(cls):
        return 'log odds ratio'

    def getPValue(self):
        pvalDict = self._pvals
        for key in pvalDict.keys():
            pvalDict[key] = SingleResultValue(
                self._getNumericFromStr(pvalDict[key]),
                '%.2e' % pvalDict[key] if type(pvalDict[key]) == float else str(pvalDict[key]))

        return self.getRemappedResultDict(pvalDict)

    def getTestStatistic(self):
        return self.getRemappedResultDict(self._testStats)

    def getFullResults(self):
        resultsFolderPath = self._resultFilesDict['output']
        mainOutput = resultsFolderPath + '/lolaResults/allEnrichments.tsv'
        fullResults = open(mainOutput).read().replace('\n','<br>\n')
        return self.getRemappedResultDict(OrderedDict([(key, fullResults) for key in self._pvals.keys()]))

    def preserveClumping(self, preserve):
        assert preserve is False

    #@takes("UniformInterface", any([None, RestrictedThroughInclusion]))
    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        assert isinstance(restrictedAnalysisUniverse, RestrictedThroughInclusion), type(restrictedAnalysisUniverse)
        self.setManualParam('useruniverse', restrictedAnalysisUniverse.trackFile.path)

    def setColocMeasure(self, colocMeasure):
        assert isinstance(colocMeasure,ColocMeasureOverlap), type(colocMeasure)
        assert colocMeasure._countWholeIntervals is True, colocMeasure._countWholeIntervals

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        pass

    def getErrorDetails(self):
        assert not self.ranSuccessfully()
        errorMessage = ''
        if self._errorMessage is not None:
            errorMessage += self._errorMessage
        if self._resultFilesDict is not None and 'stdout' in self._resultFilesDict:
            errorMessage += open(self._resultFilesDict['stdout']).read()
        if self._resultFilesDict is not None and 'stderr' in self._resultFilesDict:
            errorMessage += open(self._resultFilesDict['stderr']).read()
        if errorMessage == '':
            return 'No detailed information on error available'
        else:
            return errorMessage
