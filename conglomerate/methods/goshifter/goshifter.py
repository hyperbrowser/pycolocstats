from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict
from os import path, listdir
import gzip
import shutil

from conglomerate.core.types import SingleResultValue
from conglomerate.core.util import getTemporaryFileName
from conglomerate.methods.interface import ColocMeasureOverlap
from conglomerate.methods.method import OneVsOneMethod
from conglomerate.core.constants import GOSHIFTER_TOOL_NAME

__metaclass__ = type


class GoShifter(OneVsOneMethod):

    def __init__(self, *args, **kwargs):
        super(GoShifter, self).__init__(*args, **kwargs)
        self._testStat = {}
        self._pval = {}
        self._orginalQueryFileTitle = None
        self._orginalReferenceFileTitle = None

    def _getToolName(self):
        return GOSHIFTER_TOOL_NAME

    def _setDefaultParamValues(self):
        self.setManualParam('r', 0.9)
        # ldFile = TrackFile('/root/goshifter/hg38_eur/', 'ld file')
        self.setManualParam('l', str('/root/goshifter/hg38_eur/'))
        self.setManualParam('o', str('output'))


    def setGenomeName(self, genomeName):
        if genomeName != 'hg38':
            self.setNotCompatible()

    def setChromLenFileName(self, chromLenFileName):
        pass

    def _setQueryTrackFileName(self, trackFile):
        #bedPath = self._getBedExtendedFileName(trackFile.path)
        #self._addTrackTitleMapping(bedPath, trackFile.title)
        #self.qTrackFn = bedPath
        self._params['s'] = trackFile.path
        self._orginalQueryFileTitle = trackFile.title

    def _setReferenceTrackFileName(self, trackFile):
        if trackFile in ['prebuilt', 'LOLACore_170206']:
            self.setNotCompatible()
            return

        #bedPath = self._getBedExtendedFileName(trackFile.path)
        #self._addTrackTitleMapping(bedPath, trackFile.title)
        #self.qTrackFn = bedPath
        self._params['a'] = trackFile.path
        self._orginalReferenceFileTitle = trackFile.title

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
            sampleFile.close()
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
        tempFileNameA = getTemporaryFileName(suffix='.bed.gz')
        with open(self._params['a'], 'rb') as f_in, gzip.open(tempFileNameA, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        self._params['a'] = tempFileNameA


        #self.performGenericFileCopying()

    def setAllowOverlaps(self, allowOverlaps):
        if allowOverlaps is True:
            self.setNotCompatible()

    def _parseResultFiles(self):
        textOutPath = self.getResultFilesDict()['stdout']

        print ('textOutPath', textOutPath)

        # get p-value from stdout output
        pTF = False
        pValText = str('p-value = ')
        with open(textOutPath, 'r') as f:
            for l in f.readlines():
                if pValText in l:
                    pval = float(str(l.strip().replace(pValText, str(''))))
                    self._pval[(self._orginalQueryFileTitle, self._orginalReferenceFileTitle)] = pval
                    pTF = True


        print('self._resultFilesDict ', self._resultFilesDict)

        tsTF = False
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
                self._testStat[(self._orginalQueryFileTitle, self._orginalReferenceFileTitle)] = obsvervedval / (averageAllOtherValue / float(self._params['p']))
                tsTF = True

        print('self._pval', self._pval)
        print('self._testStat', self._testStat)
        print('getFullResults', self.getFullResults())

        if not (pTF or tsTF):
            self._ranSuccessfully = False

    @classmethod
    def getTestStatDescr(cls):
        return 'ratio of observed to average of the samples percentage of overlaping base-pairs'

    def getPValue(self):
        return self._pval

    def getTestStatistic(self):
        testStatVal = self._testStat.values()[0]
        testStatText = '<span title="' + \
                   self.getTestStatDescr() \
                   + '">' + '%.5f' % testStatVal + '</span>'
        return {(self._orginalQueryFileTitle, self._orginalReferenceFileTitle): SingleResultValue(testStatVal, testStatText)}

    def getFullResults(self):
        fullResults = open(self._resultFilesDict['stdout']).read().replace('\n', '<br>\n')

        return self.getRemappedResultDict(
            {(self._orginalQueryFileTitle, self._orginalReferenceFileTitle): str(fullResults)})

    def preserveClumping(self, preserve):
        if preserve == True:
            self.setNotCompatible()

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        #check it
        if restrictedAnalysisUniverse is not None:
            self.setNotCompatible()

    def setColocMeasure(self, colocMeasure):
        #TODO: might not be fully correct since it's only points
        if not colocMeasure or not isinstance(colocMeasure, ColocMeasureOverlap):
            self.setNotCompatible()

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        if preservationScheme is not None:
            self.setNotCompatible()

    def getErrorDetails(self):
        assert not self.ranSuccessfully()
        if self._resultFilesDict is not None and 'stderr' in self._resultFilesDict:
            return open(self._resultFilesDict['stderr']).read().replace('\n', '<br>\n')
        else:
            return 'GoShifter did not provide any error output'

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
