from conglomerate.methods.method import OneVsOneMethod
from conglomerate.tools.constants import INTERVALSTATS_TOOL_NAME
from conglomerate.tools.util import getTemporaryFileName


class IntervalStats(OneVsOneMethod):
    def _getToolName(self):
        return INTERVALSTATS_TOOL_NAME

    def _setDefaultParamValues(self):
        pass

    def _setQueryTrackFileName(self, trackFn):
        self._params['q'] = trackFn

    def _setReferenceTrackFileName(self, trackFn):
        self._params['r'] = trackFn

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

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is True

    def _parseResultFiles(self):
        #links to output files
        resultsFolderPath = self._resultFilesDict['output'] + 'output'

        self._pvals = {}
        self._pvals[(self._params['q'], self._params['r'])] = {}

        self._testStats = {}
        self._testStats[(self._params['q'], self._params['r'])] = {}

        with open(resultsFolderPath, 'r') as f:
            for line in f.readlines():
                newLine = line.strip('\n').split('\t')
                self._pvals[(self._params['q'], self._params['r'])][newLine[0]] = newLine[6]
                self._testStats[(self._params['q'], self._params['r'])][newLine[0]] = newLine[3]


    def getPValue(self):
        return self._pvals

    def getTestStatistic(self):
        return self._testStats

    def getFullResults(self):
        resultsFolderPath = self._resultFilesDict['output'] + 'output'
        return open(resultsFolderPath).read()

    def preserveClumping(self, preserve):
        #not sure yet
        assert preserve is False

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        pass

    def setColocMeasure(self, colocMeasure):
        pass

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        pass
