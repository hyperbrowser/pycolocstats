from __future__ import absolute_import, division, print_function, unicode_literals

from os import path, listdir
import gzip
import shutil

from conglomerate.core.types import TrackFile
from conglomerate.core.util import getTemporaryFileName
from conglomerate.methods.method import OneVsOneMethod
from conglomerate.core.constants import GOSHIFTER_TOOL_NAME

__metaclass__ = type


class GoShifter(OneVsOneMethod):
    def _getToolName(self):
        return GOSHIFTER_TOOL_NAME

    def _setDefaultParamValues(self):
        self.setManualParam('r', 0.9)
        # ldFile = TrackFile('/root/goshifter/hg38_eur/', 'ld file')
        self.setManualParam('l', str('/root/goshifter/hg38_eur/'))


    def setGenomeName(self, genomeName):
        if genomeName != 'hg38':
            self.setNotCompatible()

    def setChromLenFileName(self, chromLenFileName):
        pass

    def _setQueryTrackFileName(self, trackFile):
        bedPath = self._getBedExtendedFileName(trackFile.path)
        self._addTrackTitleMapping(bedPath, trackFile.title)
        self.qTrackFn = bedPath
        self._params['s'] = bedPath
        self._orginalQueryFile = trackFile.title

    def _setReferenceTrackFileName(self, trackFile):
        bedPath = self._getBedExtendedFileName(trackFile.path)
        self._addTrackTitleMapping(bedPath, trackFile.title)
        self.qTrackFn = bedPath
        self._params['a'] = bedPath
        self._orginalReferenceFile = trackFile.title

    def prepareInputData(self):

        #modify file self._params['s'] file into snpmap file
        queryTrackIsPoints = True
        queryTracHaveRS = True

        contents = []
        contents.append(['SNP', 'Chrom', 'BP'])
        with open(self._params['s'], 'r') as f:
            for line in f.readlines():
                newl = line.strip('\n').split('\t')
                #check if it is a .bed file with at least 4 columns
                if len(newl) >= 4:
                    #provide proper order for snpmap file
                    if int(newl[2]) - int(newl[1]) != 1:
                        queryTrackIsPoints = False
                        break
                    if 'rs' not in newl[3]:
                        queryTracHaveRS = False
                        break
                    contents.append([newl[3], newl[0], newl[1]])
                else:
                    queryTracHaveRS = False
                    break

        if queryTrackIsPoints and queryTracHaveRS:
            tempFileName = getTemporaryFileName()
            print (tempFileName)
            sampleFile = open(tempFileName, 'w')
            for c in contents:
                sampleFile.write('\t'.join(c) + '\n')
            sampleFile.flush()
            self._params['s'] = sampleFile.name

        if not queryTrackIsPoints:
            self.setNotCompatible()
            #raise Exception('GOShifter only works with single base pairs as input regions')
        if not queryTracHaveRS:
            self.setNotCompatible()
            #raise Exception('GOShifter only works were column name is filled by rs')


        #check if self._params['a'] is not empty or is a bed file with at least 3 columns
        # emptyFile = path.getsize(self._params['a'])
        # if emptyFile <= 0:
        #     self.setNotCompatible()

        # with open(self._params['a'], 'r') as f:
        #     for line in f.readlines():
        #         vals = line.strip().split()
        #         if len(vals) < 3:
        #             self.setNotCompatible()

        # gz file annotation
        tempFileNameA = getTemporaryFileName()
        with open(self._params['a'], 'rb') as f_in, gzip.open(tempFileNameA, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        self._params['a'] = tempFileNameA
        print (self._params['a'])

        self.performGenericFileCopying()

    def setAllowOverlaps(self, allowOverlaps):
        if allowOverlaps is True:
            self.setNotCompatible()

    def _parseResultFiles(self):
        textOutPath = self.getResultFilesDict()['stdout']

        self._pvals = {}
        # get p-value from stdout output
        self._pvals[(self._orginalQueryFile, self._orginalReferenceFile)] = -1
        pValText = 'p-value = '
        with open(textOutPath, 'r') as f:
            for l in f.readlines():
                if pValText in l:
                    print(l.strip('\n').replace(pValText, ''))
                    self._pvals[(self._orginalQueryFile, self._orginalReferenceFile)] = l.strip('\n').replace(pValText, '')

        self._testStats = {}
        self._testStats[(self._orginalQueryFile, self._orginalReferenceFile)] = -1
        for fi in listdir(path.join(self._resultFilesDict['output'])):
            if 'nperm10.enrich' in fi:
                obsvervedval = 0
                averageAllOtherValue = 0
                with open(path.join(self._resultFilesDict['output'], fi), 'r') as f:
                    for numL, l in enumerate(f.readlines()):
                        if numL == 1:
                            obsvervedval = float(l.strip().split('\t')[3])
                        if numL > 1:
                            averageAllOtherValue += float(l.strip().split('\t')[3])
                print (obsvervedval / (averageAllOtherValue/float(self._params['p'])))
                self._testStats[(self._orginalQueryFile, self._orginalReferenceFile)] = obsvervedval / (averageAllOtherValue/float(self._params['p']))

        if self._pvals[(self._orginalQueryFile, self._orginalReferenceFile)] != -1:
            self._ranSuccessfully = True
        if self._testStats[(self._orginalQueryFile, self._orginalReferenceFile)] != -1:
            self._ranSuccessfully = True

    def getPValue(self):
        return self._pvals

    def getTestStatistic(self):
        return self._testStats

    def getFullResults(self):
        return open(self.getResultFilesDict()['stdout']).read()

    def preserveClumping(self, preserve):
        if preserve == True:
            self.setNotCompatible()

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        #check it
        if restrictedAnalysisUniverse is not None:
            self.setNotCompatible()

    def setColocMeasure(self, colocMeasure):
        #take it from HB
        #support bp and all region which is point
        pass

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        if preservationScheme is not None:
            self.setNotCompatible()

    def getErrorDetails(self):
        assert not self.ranSuccessfully()

    def setRuntimeMode(self, mode):
        #take from paper
        if mode =='quick':
            numPerm = 10
        elif mode == 'medium':
            numPerm = 100
        elif mode == 'accurate':
            numPerm = 1000
        else:
            raise Exception('Invalid mode')
        self.setManualParam('p', numPerm)