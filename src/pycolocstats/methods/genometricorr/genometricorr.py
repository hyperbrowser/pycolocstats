from __future__ import absolute_import, division, print_function, unicode_literals

from pycolocstats.methods.interface import ColocMeasureOverlap
from pycolocstats.methods.method import OneVsOneMethod
from pycolocstats.core.types import SingleResultValue, TrackFile
from pycolocstats.core.constants import GENOMETRICORR_TOOL_NAME

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

    def _setQueryTrackFileName(self, trackFile):
        bedPath = self._getBedExtendedFileName(trackFile.path)
        self._addTrackTitleMapping(bedPath, trackFile.title)
        self._params['query'] = bedPath

    def _setReferenceTrackFileName(self, trackFile):
        from pycolocstats.tools.tracks import refTrackCollRegistry
        if refTrackCollRegistry.isPartOfTrackCollSpec(trackFile):
            self.setNotCompatible()
            return

        if isinstance(trackFile, TrackFile):
            trackFn = trackFile.path
        else:
            trackFn = trackFile
        bedPath = self._getBedExtendedFileName(trackFn)
        if isinstance(trackFile, TrackFile):
            self._addTrackTitleMapping(bedPath, trackFile.title)
        self._params['reference'] = bedPath

    def setAllowOverlaps(self, allowOverlaps):
        if not (allowOverlaps is False):
            self.setNotCompatible()

    def _parseResultFiles(self):
        self._results = self._parseGenometricorrStdout()

    def _parseGenometricorrStdout(self):
        resultsFolderPath = self._resultFilesDict['output']
        mainOutput = resultsFolderPath + "/GenometriCorr_Output.txt"
        self._fullResults = open(mainOutput).read().replace('\n','<br>\n')
        fullTable = [line.split() for line in open(mainOutput)]
        colheaders = fullTable[0][1:]
        resultTable = fullTable[1:]
        data = {}
        for row in resultTable:
            rowheader = row[0]
            rowdata = row[1:]
            rowdict = dict(zip(colheaders, rowdata))
            data[rowheader] = rowdict
        return data

    def getPValue(self):
        rowDict = self._results['jaccard.measure.p.value']
        pVal = rowDict['awhole'] if 'awhole' in rowDict else list(rowDict.values())[0]
        return self.getRemappedResultDict(
            {(self._params['query'], self._params['reference']):
                 SingleResultValue(self._getNumericFromStr(pVal), pVal)})

    def getTestStatistic(self):
        rowDict = self._results['projection.test.obs.to.exp']
        numericResult = float(rowDict['awhole'] if 'awhole' in rowDict else list(rowDict.values())[0])
        testStat = '<span title="' + \
                   self.getTestStatDescr() \
                   + '">' + \
                   self._getFormattedVal(numericResult) + '</span>'
        return self.getRemappedResultDict(
            {(self._params['query'], self._params['reference']): SingleResultValue(numericResult, testStat)})
        #return self.getRemappedResultDict({(self._params['query'],self._params['reference']):self._results['jaccard.measure']['awhole']})

    @classmethod
    def getTestStatDescr(cls):
        return 'ratio of observed to expected (according to projection test)'

    def getFullResults(self):
        return self.getRemappedResultDict({(self._params['query'],self._params['reference']): self._fullResults})

    def preserveClumping(self, preserve):
        pass

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        if restrictedAnalysisUniverse is not None:
            self.setNotCompatible()

    def setColocMeasure(self, colocMeasure):
        if not isinstance(colocMeasure, ColocMeasureOverlap):
            self.setNotCompatible()

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        pass

    def getErrorDetails(self):
        assert not self.ranSuccessfully()
        if self._resultFilesDict is not None and 'stderr' in self._resultFilesDict:
            return open(self._resultFilesDict['stderr']).read().replace('\n','<br>\n')
        else:
            return 'Genometricorr did not provide any error output'

    def setRuntimeMode(self, mode):
        if mode =='quick':
            numPerm = 20
        elif mode == 'medium':
            numPerm = 100
        elif mode == 'accurate':
            numPerm = 500
        else:
            raise Exception('invalid mode')
        self.setManualParam('ecdfPermNum', numPerm)
        self.setManualParam('meanPermNum', numPerm)
        self.setManualParam('jaccardPermNum', numPerm)
