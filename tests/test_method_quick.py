import os
import pytest

from pycolocstats.core.types import TrackFile
from pycolocstats.methods.genometricorr.genometricorr import GenometriCorr
from pycolocstats.methods.giggle.giggle import Giggle
from pycolocstats.methods.goshifter.goshifter import GoShifter
from pycolocstats.methods.intervalstats.intervalstats import IntervalStats
from pycolocstats.methods.multimethod import MultiMethod
from pycolocstats.methods.stereogene.stereogene import StereoGene
from pycolocstats.tools.runner import runAllMethods
from tests import TEST_RESOURCES_DIR
from tests.test_method import TestMethodsBase


@pytest.fixture(scope='function')
def tracks():
    return [
        TrackFile(os.path.join(TEST_RESOURCES_DIR, 'test_track1.bed'), 'track1'),
        TrackFile(os.path.join(TEST_RESOURCES_DIR, 'test_track2.bed'), 'track2'),
        TrackFile(os.path.join(TEST_RESOURCES_DIR, 'test_track3.bed'), 'track3'),
        TrackFile(os.path.join(TEST_RESOURCES_DIR, 'test_track4.bed'), 'track4'),
        TrackFile(os.path.join(TEST_RESOURCES_DIR, 'test_track5.bed'), 'track5'),
        TrackFile(os.path.join(TEST_RESOURCES_DIR, 'test_track6.bed'), 'track6'),
        TrackFile(os.path.join(TEST_RESOURCES_DIR, 'test_track7.bed'), 'track7'),
        TrackFile(os.path.join(TEST_RESOURCES_DIR, 'test_track8.bed'), 'track8'),
        TrackFile(os.path.join(TEST_RESOURCES_DIR, 'test_track9.bed'), 'track9'),
        TrackFile(os.path.join(TEST_RESOURCES_DIR, 'test_track10.bed'), 'track10'),
    ]


@pytest.fixture(scope='function')
def chrLenFile():
    return os.path.join(TEST_RESOURCES_DIR, 'test_chrom_lengths_2.tabular')


@pytest.mark.usefixtures('chrLenFile', 'tracks')
class TestMethods(TestMethodsBase):

    def testStereoGene_OneVsOne(self, chrLenFile, tracks):
        method = StereoGene()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        method.setManualParam('wSize', 20)
        method.setManualParam('bin', 5)
        method.setManualParam('kernelSigma', 10.0)
        runAllMethods([method])
        # self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(1, method)
        print(method.getFullResults())

    def testStereoGene_OneVsOne_header_in_data(self, chrLenFile, tracks):
        method = StereoGene()
        method.setQueryTrackFileNames([tracks[6]])
        method.setReferenceTrackFileNames([tracks[7]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        method.setManualParam('wSize', 20)
        method.setManualParam('bin', 5)
        method.setManualParam('kernelSigma', 10.0)
        runAllMethods([method])
        # self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(1, method)

    def testStereoGene_OneVsMany(self, chrLenFile, tracks):
        refTracks = [tracks[0], tracks[1]]
        qTracks = [tracks[2]]
        method = MultiMethod(StereoGene, qTracks, refTracks)
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        method.setManualParam('wSize', 20)
        method.setManualParam('bin', 5)
        method.setManualParam('kernelSigma', 10.0)
        runAllMethods([method])
        # self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(2, method)

    def testStereoGene_OneVsMany_pickling(self, chrLenFile, tracks):
        refTracks = [tracks[0], tracks[1]]
        qTracks = [tracks[2]]
        method = MultiMethod(StereoGene, qTracks, refTracks)
        from pickle import dumps, loads
        methodStr = dumps(method)
        method = loads(methodStr)
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        method.setManualParam('wSize', 20)
        method.setManualParam('bin', 5)
        method.setManualParam('kernelSigma', 10.0)
        runAllMethods([method])
        # self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(2, method)

    def testGenometriCorr_OneVsOne(self, chrLenFile, tracks):
        # raise Exception('With current setup, too long running time to function as unit test')
        method = GenometriCorr()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('ecdfPermNum', 5)
        method.setManualParam('meanPermNum', 5)
        method.setManualParam('jaccardPermNum', 5)
        runAllMethods([method])
        # self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(1, method)
        method.getFullResults()

    def testGenometriCorr_OneVsOne_header_in_data(self, chrLenFile, tracks):
        # raise Exception('With current setup, too long running time to function as unit test')
        method = GenometriCorr()
        method.setQueryTrackFileNames([tracks[6]])
        method.setReferenceTrackFileNames([tracks[7]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('ecdfPermNum', 5)
        method.setManualParam('meanPermNum', 5)
        method.setManualParam('jaccardPermNum', 5)
        runAllMethods([method])
        # self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(1, method)

    def testIntervalStats_OneVsOne(self, chrLenFile, tracks):
        method = IntervalStats()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('o', 'output')
        runAllMethods([method])
        self._assertMethodResultsSize(1, method)

    def testIntervalStats_OneVsMany(self, chrLenFile, tracks):
        method = MultiMethod(IntervalStats, [tracks[0]], tracks[1:3])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('o', 'output')
        runAllMethods([method])
        self._assertMethodResultsSize(2, method)

    def testGiggle_OneVsMany(self, chrLenFile, tracks):
        method = Giggle()
        method.setQueryTrackFileNames([tracks[0]])
        refTracks = [tracks[1], tracks[2]]
        method.setReferenceTrackFileNames(refTracks)
        # method = MultiMethod(Giggle, [tracks[8]], refTracks)
        method.setChromLenFileName(chrLenFile)
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(len(refTracks), method)

    @pytest.mark.skip("Giggle tool fails")
    def testGiggle_OneVsMany_header_in_data(self, chrLenFile, tracks):
        method = Giggle()
        method.setQueryTrackFileNames([tracks[6]])
        refTracks = [tracks[7], tracks[8]]
        method.setReferenceTrackFileNames(refTracks)
        # method = MultiMethod(Giggle, [tracks[8]], refTracks)
        method.setChromLenFileName(chrLenFile)
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(len(refTracks), method)

    def testGoShifter(self, chrLenFile, tracks):
        method = GoShifter()
        # snpmap = os.path.join(TEST_RESOURCES_DIR, 'snpmap.tabular'
        # annotation = os.path.join(TEST_RESOURCES_DIR, 'annotation.bed.gz'
        # proxies = os.path.join(TEST_RESOURCES_DIR, 'proxies.txt'
        method.setQueryTrackFileNames([tracks[4]])
        method.setReferenceTrackFileNames([tracks[5]])
        # method.setManualParam('s', snpmap)
        # method.setManualParam('a', annotation)
        method.setManualParam('l', '/root/goshifter/hg38_eur/')
        method.setManualParam('p', 10)
        method.setManualParam('o', 'output')
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(1, method)

    def testGoShifter_header_in_data(self, chrLenFile, tracks):
        method = GoShifter()
        # snpmap = os.path.join(TEST_RESOURCES_DIR, 'snpmap.tabular'
        # annotation = os.path.join(TEST_RESOURCES_DIR, 'annotation.bed.gz'
        # proxies = os.path.join(TEST_RESOURCES_DIR, 'proxies.txt'
        method.setQueryTrackFileNames([tracks[9]])
        method.setReferenceTrackFileNames([tracks[5]])
        # method.setManualParam('s', snpmap)
        # method.setManualParam('a', annotation)
        method.setManualParam('l', '/root/goshifter/hg38_eur/')
        method.setManualParam('p', 10)
        method.setManualParam('o', 'output')
        runAllMethods([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(1, method)

    # @staticmethod
    # def _assertMethodResultsSize(expectedResulstNr, method):
    #     assert expectedResulstNr == len(method.getTestStatistic()), \
    #         "%s: Expected %i test statistic results got %i (got teststat: %s)" % (
    #             str(method), expectedResulstNr, len(method.getTestStatistic()), method.getTestStatistic())
    #     assert expectedResulstNr == len(method.getPValue()), \
    #         "%s: Expected %i p-values got %i" % (str(method), expectedResulstNr, len(method.getPValue()))
    #
    # @staticmethod
    # def _printResultFiles(method, keys):
    #     if isinstance(method, MultiMethod):
    #         resultFilesDictList = method.getResultFilesDictList()
    #     else:
    #         resultFilesDictList = [method.getResultFilesDict()]
    #
    #     for resultFilesDict in resultFilesDictList:
    #         for key in keys:
    #             assert key in resultFilesDict, (key,resultFilesDict)
    #             print(key)
    #             print('------')
    #             print('Local path: ' + resultFilesDict[key])
    #             print('------')
    #             print('\n'.join(os.listdir(resultFilesDict[key])) if key == 'output'
    #             else open(resultFilesDict[key]).read())
