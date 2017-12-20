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

    def _getBedExtendedFileName(self, trackFn): #TODO: Replace with better handling of temporary files
        from tempfile import mkdtemp
        import os
        os.get
        import shutil
        #bedPath = os.path.join(mkdtemp(), trackFn.replace('.dat','.bed'))
        bedPath = '/tmp/adHocBed/' + os.path.basename(trackFn).replace('.dat','.bed')
        #shutil.copytree(src=trackFn, dst=bedFn,symlinks=True)
        shutil.copy(src=trackFn, dst=bedPath)
        return bedPath

    def _setQueryTrackFileName(self, trackFn):
        bedPath = self._getBedExtendedFileName(trackFn)
        self._params['query'] = bedPath


    def _setReferenceTrackFileName(self, trackFn):
        bedPath = self._getBedExtendedFileName(trackFn)
        self._params['reference'] = bedPath

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is False

    def _parseResultFiles(self):
        self._results = self._parseGenometricorrStdout()

    def _parseGenometricorrStdout(self):
        resultsFolderPath = self._resultFilesDict['output']
        mainOutput = resultsFolderPath + "/GenometriCorr_Output.txt"
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
        return {(self._params['query'],self._params['reference']): self._results['jaccard.measure.p.value']['awhole']}

    def getTestStatistic(self):
        return {(self._params['query'],self._params['reference']):self._results['jaccard.measure']['awhole']}

    def getFullResults(self):
        return {(self._params['query'],self._params['reference']): "Full results for Genometricorr not implemented.."}

    def preserveClumping(self, preserve):
        pass

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        pass

    def setColocMeasure(self, colocMeasure):
        pass

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        pass

    def getErrorDetails(self):
        assert not self.ranSuccessfully()
        return open(self._resultFilesDict['stderr']).read().replace('\n','<br>\n')
