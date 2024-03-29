from tempfile import NamedTemporaryFile

import os
import pytest

from tests import TEST_RESOURCES_DIR
from pycolocstats.methods.genometricorr.genometricorr import GenometriCorr
from pycolocstats.methods.giggle.giggle import Giggle
from pycolocstats.methods.interface import RestrictedThroughInclusion
from pycolocstats.methods.intervalstats.intervalstats import IntervalStats
from pycolocstats.methods.lola.lola import LOLA
from pycolocstats.methods.multimethod import MultiMethod
from pycolocstats.methods.stereogene.stereogene import StereoGene
from pycolocstats.core.types import TrackFile
from pycolocstats.tools.runner import runAllMethods


@pytest.fixture(scope='function')
def tracks():
    return [TrackFile(os.path.join(TEST_RESOURCES_DIR, 'H3K4me1_no_overlaps.bed'), 't1'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'H3K4me3_no_overlaps.bed'), 't2'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'H3K4me1_with_overlaps.bed'), 't3'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'H3K4me3_with_overlaps.bed'), 't4'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'H3K4me1_no_overlaps.bed.gz'), 't5'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'H3K4me3_no_overlaps.bed.gz'), 't6'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'H3K4me1_with_overlaps.bed.gz'), 't7'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'H3K4me3_with_overlaps.bed.gz'), 't8'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'H3K4me1_no_overlaps_cropped.bed'), 't9'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'H3K4me1_no_overlaps_large.bed.gz'), 't10'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'H3K4me3_no_overlaps_large.bed.gz'), 't11'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'Refseq_Genes_cropped.bed.gz'), 't12'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'Ensembl_Genes_cropped.bed.gz'), 't13'),
            TrackFile(os.path.join(TEST_RESOURCES_DIR, 'H3K4me3_no_overlaps_cropped.bed'), 't14')]


@pytest.fixture(scope='function')
def chrLenFile():
    return os.path.join(TEST_RESOURCES_DIR, 'chrom_lengths.tabular')


class TestMethodsBase(object):
    @staticmethod
    def _printResultFiles(method, keys):
        if isinstance(method, MultiMethod):
            resultFilesDictList = method.getResultFilesDictList()
        else:
            resultFilesDictList = [method.getResultFilesDict()]

        for resultFilesDict in resultFilesDictList:
            for key in keys:
                assert key in resultFilesDict, (key, resultFilesDict)
                print(key)
                print('------')
                print('Local path: ' + resultFilesDict[key])
                print('------')
                print('\n'.join(os.listdir(resultFilesDict[key])) if key == 'output'
                      else open(resultFilesDict[key]).read())

    @staticmethod
    def _assertMethodResultsSize(expectedResulstNr, method):
        assert expectedResulstNr == len(method.getTestStatistic()), \
            "%s: Expected %i test statistic results got %i (got teststat: %s)" % (
                str(method), expectedResulstNr, len(method.getTestStatistic()), method.getTestStatistic())
        assert expectedResulstNr == len(method.getPValue()), \
            "%s: Expected %i p-values got %i" % (str(method), expectedResulstNr, len(method.getPValue()))


@pytest.mark.usefixtures('chrLenFile', 'tracks')
class TestMethods(TestMethodsBase):
    def testUnified(self, tracks, chrLenFile):
        # define tracks and methods (will in real runs come in from GUI)
        queryTrack = [tracks[0]]
        refTracks = [tracks[1], tracks[2]]
        methodClasses = [GenometriCorr, StereoGene]

        # create selections (will in real runs come in from GUI)
        allowOverlapChoiceList = [('setAllowOverlaps', False), ('setAllowOverlaps', True)]
        preserveClumpingChoiceList = [('preserveClumping', False), ('preserveClumping', True)]
        chrLenList = [('setChromLenFileName', chrLenFile)]
        selectionsValues = [allowOverlapChoiceList, preserveClumpingChoiceList, chrLenList]
        from pycolocstats.tools.method_compatibility import getCompatibleMethodObjects
        workingMethodObjects = getCompatibleMethodObjects(selectionsValues, queryTrack, refTracks, methodClasses)
        print(len(workingMethodObjects), [wmo for wmo in workingMethodObjects])

        # runAllMethodsInSequence(workingMethodObjects)
        # for workingMethod in workingMethodObjects:
        #     self._printResultFiles(workingMethod, ['stderr', 'stdout', 'output'])

    def testGenometriCorr(self, chrLenFile, tracks):
        # raise Exception('With current setup, too long running time to function as unit test')
        method = GenometriCorr()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('ecdfPermNum', 5)
        method.setManualParam('meanPermNum', 5)
        method.setManualParam('jaccardPermNum', 5)
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        print(method.getPValue())
        print(method.getTestStatistic())

    def testStereoGene(self, chrLenFile, tracks):
        method = StereoGene()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(1, method)

    def testStereoGeneOneVsMulti(self, chrLenFile, tracks):
        refTracks = [tracks[2], tracks[3]]
        method = MultiMethod(StereoGene, [tracks[0]], refTracks)
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(len(refTracks), method)

    def testStereoGeneMultiVsMulti(self, chrLenFile, tracks):
        # raise Exception('With current setup, too long running time to function as unit test')

        qTracks = [tracks[0], tracks[1]]
        refTracks = [tracks[2], tracks[3]]
        method = MultiMethod(StereoGene, qTracks, refTracks)
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(len(qTracks) * len(refTracks), method)

    def testIntervalStats(self, chrLenFile, tracks):
        method = IntervalStats()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('o', 'output')
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testIntervalStatsMultiOneVsMany(self, chrLenFile, tracks):
        method = MultiMethod(IntervalStats, [tracks[0]], [tracks[2], tracks[3]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('o', 'output')
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testIntervalStatsMultiManyVsMany(self, chrLenFile, tracks):
        method = MultiMethod(IntervalStats, [tracks[0], tracks[1]], [tracks[2], tracks[3]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('o', 'output')
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testIntervalStatsMultipleMethods(self, chrLenFile, tracks):
        method1 = IntervalStats()
        method1.setQueryTrackFileNames([tracks[0]])
        method1.setReferenceTrackFileNames([tracks[1]])
        method1.setChromLenFileName(chrLenFile)
        method1.setManualParam('o', 'output')

        method2 = MultiMethod(IntervalStats, [tracks[0]], [tracks[2], tracks[3]])
        method2.setChromLenFileName(chrLenFile)
        method2.setManualParam('o', 'output')

        method3 = MultiMethod(IntervalStats, [tracks[0], tracks[1]], [tracks[2], tracks[3]])
        method3.setChromLenFileName(chrLenFile)
        method3.setManualParam('o', 'output')

        runAllMethods([method1, method2, method3])

        self._printResultFiles(method1, ['stderr', 'stdout', 'output'])
        self._printResultFiles(method2, ['stderr', 'stdout', 'output'])
        self._printResultFiles(method3, ['stderr', 'stdout', 'output'])

    def testGiggleDynamic(self, chrLenFile, tracks):
        method = Giggle()
        method.setQueryTrackFileNames([tracks[8]])
        refTracks = [tracks[13], tracks[11], tracks[12]]
        method.setReferenceTrackFileNames(refTracks)
        # method = MultiMethod(Giggle, [tracks[8]], refTracks)
        method.setChromLenFileName(chrLenFile)
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(len(refTracks), method)

    def testGiggleReference(self, chrLenFile, tracks):
        method = Giggle()
        method.setQueryTrackFileNames([tracks[9]])
        method.setManualParam('trackIndex', 'LOLACore_170206')
        method.setManualParam('genome', 'hg19')
        method.setManualParam('trackCollection', 'codex')
        method.setChromLenFileName(chrLenFile)
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        raise Exception("This is now failing silently")

    def testGiggleMultiManyVsMany(self, chrLenFile, tracks):
        refTracks = [tracks[11], tracks[12]]
        qTracks = [tracks[9], tracks[10]]
        method = MultiMethod(Giggle, qTracks, refTracks)
        method.setChromLenFileName(chrLenFile)
        runAllMethods([method])
        expectedResulstNr = len(qTracks) * len(refTracks)
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(expectedResulstNr, method)

    def testLOLADynamic(self, chrLenFile, tracks):
        # raise Exception('With current setup, too long running time to function as unit test') #ok with lola_test
        method = LOLA()
        method.setQueryTrackFileNames([tracks[8]])
        method.setReferenceTrackFileNames([tracks[2], tracks[3]])
        method.setRestrictedAnalysisUniverse(RestrictedThroughInclusion(tracks[0]))
        method.preserveClumping(False)
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        method.getFullResults()

    def testLOLAReference(self, chrLenFile, tracks):
        method = LOLA()
        method.setQueryTrackFileNames([tracks[8]])
        method.setRestrictedAnalysisUniverse(RestrictedThroughInclusion(tracks[0]))
        method.setManualParam('trackIndex', 'LOLACore_170206')
        method.setManualParam('genome', 'hg19')
        method.setManualParam('trackCollection', 'codex')
        method.preserveClumping(False)
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    @staticmethod
    def _getSampleFileName(contents):
        sampleFile = NamedTemporaryFile(mode='w+', dir='/tmp', suffix='.bed')
        sampleFile.write(contents)
        sampleFile.flush()
        return sampleFile
