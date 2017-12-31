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

    def _setQueryTrackFileName(self, trackFile):
        bedPath = self._getBedExtendedFileName(trackFile.path)
        self._addTrackTitleMapping(bedPath, trackFile.title)
        self._params['query'] = bedPath


    def _setReferenceTrackFileName(self, trackFile):
        from conglomerate.tools.TrackFile import TrackFile
        if isinstance(trackFile, TrackFile):
            trackFn = trackFile.path
        else:
            trackFn = trackFile
        assert trackFn not in ['prebuilt', 'LOLACore_170206']
        bedPath = self._getBedExtendedFileName(trackFn)
        if isinstance(trackFile, TrackFile):
            self._addTrackTitleMapping(bedPath, trackFile.title)
        self._params['reference'] = bedPath

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is False

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
        return self.getRemappedResultDict({(self._params['query'],self._params['reference']): self._results['jaccard.measure.p.value']['awhole']})

    def getTestStatistic(self):
        testStat = '<a href="" title="ratio of observed to expected (according to projection test)">' + '%.2f' % float(self._results['projection.test.obs.to.exp']['awhole']) + '</a>'
        return self.getRemappedResultDict(
            {(self._params['query'], self._params['reference']): testStat})
        #return self.getRemappedResultDict({(self._params['query'],self._params['reference']):self._results['jaccard.measure']['awhole']})

    def getFullResults(self):
        return self.getRemappedResultDict({(self._params['query'],self._params['reference']): self._fullResults})

    def preserveClumping(self, preserve):
        pass

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        assert restrictedAnalysisUniverse is None, restrictedAnalysisUniverse

    def setColocMeasure(self, colocMeasure):
        pass

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
            raise
        self.setManualParam('ecdfPermNum', numPerm)
        self.setManualParam('meanPermNum', numPerm)
        self.setManualParam('jaccardPermNum', numPerm)
