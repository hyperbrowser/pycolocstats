from __future__ import absolute_import, division, print_function, unicode_literals

from os import path, listdir

from conglomerate.core.util import getTemporaryFileName
from conglomerate.methods.method import OneVsOneMethod
from conglomerate.core.constants import GOSHIFTER_TOOL_NAME

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


    def _setQueryTrackFileName(self, trackFile):
        pass

    def _setReferenceTrackFileName(self, trackFn):
        pass

    def prepareInputData(self):
        #TODO: Diana!: Here you will transform from bed to snpmap or whatever..
        # queryTrackIsPoints = True #TODO: Diana!: Here you should instead check whether it is really points in the query track

        queryTrackIsPoints = True
        queryTrackDoesNotHaveRS = True

        contents = []
        with open(self._params['s'], 'r') as f:
            for line in f.readlines():
                newl = line.strip('\n').split('\t')
                if len(newl) >= 4:
                    #provide proper order for snpmap file
                    if int(newl[1] - newl[0]) != 1:
                        queryTrackIsPoints = False
                    contents.append([newl[0], newl[1], newl[2]])
                else:
                    queryTrackDoesNotHaveRS = False

        if queryTrackIsPoints and queryTrackDoesNotHaveRS:
            tempFileName = getTemporaryFileName()
            sampleFile = open(tempFileName, 'w')
            for c in contents:
                sampleFile.write('\t'.join(c) + '\n')
            sampleFile.flush()

            self._params['s'] = sampleFile.name


        if not queryTrackIsPoints:
            raise Exception('GOShifter only works with single base pairs as input regions')
        if not queryTrackDoesNotHaveRS:
            raise Exception('GOShifter only works were column name is filled by rs')
        self.performGenericFileCopying()

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is True

    def _parseResultFiles(self):
        self.setRunSuccessStatus(False, str('ssss'))
        # textOut = self.getResultFilesDict()['stdout']
        #
        # self._pvals={}
        #
        # #get p-value from stdout output
        # pValText = 'p-value = '
        # valStart = textOut.find(pValText)
        # valEnd = textOut.find('Detailed')
        # self._pvals[(self._params['a'], self._params['o'])] = textOut[valStart + len(pValText):valEnd]
        # self._testStats[(self._params['a'], self._params['o'])] = -1
        #
        # for fi in listdir(path.join(self._resultFilesDict['output'])):
        #     if 'nperm10.enrich' in fi:
        #         with open(path.join(self._resultFilesDict['output'], fi), 'r') as f:
        #             self._testStats[(self._params['a'], self._params['o'])] = f.readlines()[1].split('\t')[1]


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
