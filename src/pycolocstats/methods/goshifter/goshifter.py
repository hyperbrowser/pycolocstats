from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict
from os import path, listdir
import gzip
import shutil

from pycolocstats.core.types import SingleResultValue
from pycolocstats.core.util import getTemporaryFileName
from pycolocstats.methods.interface import ColocMeasureOverlap
from pycolocstats.methods.method import OneVsOneMethod
from pycolocstats.core.constants import GOSHIFTER_TOOL_NAME

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
        self.setManualParam('r', 0.8)
        self.setManualParam('l', str('/root/goshifter/hg38_eur/'))
        self.setManualParam('o', str('output'))


    def setGenomeName(self, genomeName):
        if genomeName != 'hg38':
            self.setNotCompatible()

    def setChromLenFileName(self, chromLenFileName):
        pass

    def _setQueryTrackFileName(self, trackFile):
        self._params['s'] = trackFile.path
        self._orginalQueryFileTitle = trackFile.title

    def _setReferenceTrackFileName(self, trackFile):
        from pycolocstats.tools.tracks import refTrackCollRegistry
        if refTrackCollRegistry.isPartOfTrackCollSpec(trackFile):
            self.setNotCompatible()
            return
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
                #check if there is any header
                if not line.startswith('chr'):
                    continue
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

        # gz file annotation
        tempFileNameA = getTemporaryFileName(suffix='.bed.gz')

        #check if there is any header in the file
        contentAnnotationFile = ''
        with open(self._params['a'], 'r') as f:
            for line in f.readlines():
                if not line.startswith('chr'):
                    continue
                contentAnnotationFile += line

        g = gzip.open(tempFileNameA, 'w')
        g.write(contentAnnotationFile)
        g.close()
        self._params['a'] = tempFileNameA

    def setAllowOverlaps(self, allowOverlaps):
        if allowOverlaps is True:
            self.setNotCompatible()

    def _parseResultFiles(self):
        textOutPath = self.getResultFilesDict()['stdout']

        # get p-value from stdout output
        pTF = False
        pValText = str('p-value = ')
        with open(textOutPath, 'r') as f:
            for l in f.readlines():
                if pValText in l:
                    pval = float(str(l.strip().replace(pValText, str(''))))
                    self._pval[(self._orginalQueryFileTitle, self._orginalReferenceFileTitle)] = pval
                    pTF = True

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

        if not (pTF or tsTF):
            self._ranSuccessfully = False

    @classmethod
    def getTestStatDescr(cls):
        return 'ratio of observed to average of the samples percentage of overlaping base-pairs'

    def getPValue(self):
        pvalDict = self._pval
        for key in pvalDict.keys():
            pvalDict[key] = SingleResultValue(
                self._getNumericFromStr(pvalDict[key]),
                self._getFormattedVal(pvalDict[key]) if type(pvalDict[key]) == float else str(pvalDict[key]))

        return self.getRemappedResultDict(pvalDict)

    def getTestStatistic(self):
        testStatVal = self._testStat.values()[0]
        testStatText = '<span title="' + \
                   self.getTestStatDescr() \
                   + '">' + self._getFormattedVal(testStatVal) + '</span>'
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
        if mode =='quick':
            numPerm = 10
        elif mode == 'medium':
            numPerm = 100
        elif mode == 'accurate':
            numPerm = 1000
        else:
            raise Exception('Invalid mode')
        self.setManualParam('p', numPerm)
