from itertools import product
from tempfile import NamedTemporaryFile

import os
import pkg_resources
import pytest

from conglomerate.methods.genometricorr.genometricorr import GenometriCorr
from conglomerate.methods.giggle.giggle import Giggle
from conglomerate.methods.goshifter.goshifter import GoShifter
from conglomerate.methods.interface import RestrictedThroughInclusion
from conglomerate.methods.intervalstats.intervalstats import IntervalStats
from conglomerate.methods.lola.lola import LOLA
from conglomerate.methods.multimethod import MultiMethod
from conglomerate.methods.stereogene.stereogene import StereoGene
from conglomerate.tools.TrackFile import TrackFile
from conglomerate.tools.runner import runAllMethodsInSequence


@pytest.fixture(scope='function')
def tracks():
    return [TrackFile(pkg_resources.resource_filename('tests.resources', 'H3K4me1_no_overlaps.bed'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'H3K4me3_no_overlaps.bed'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'H3K4me1_with_overlaps.bed'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'H3K4me3_with_overlaps.bed'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'H3K4me1_no_overlaps.bed.gz'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'H3K4me3_no_overlaps.bed.gz'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'H3K4me1_with_overlaps.bed.gz'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'H3K4me3_with_overlaps.bed.gz'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'H3K4me1_no_overlaps_cropped.bed'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'H3K4me1_no_overlaps_large.bed.gz'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'H3K4me3_no_overlaps_large.bed.gz'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'Refseq_Genes_cropped.bed.gz'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'Ensembl_Genes_cropped.bed.gz'),''),
            TrackFile(pkg_resources.resource_filename('tests.resources', 'H3K4me3_no_overlaps_cropped.bed'),'')]


@pytest.fixture(scope='function')
def chrLenFile():
    return pkg_resources.resource_filename('tests.resources', 'chrom_lengths.tabular')


@pytest.mark.usefixtures('chrLenFile', 'tracks')
class TestMethods(object):
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
        from conglomerate.tools.method_compatibility import getCompatibleMethodObjects
        workingMethodObjects = getCompatibleMethodObjects(selectionsValues, queryTrack, refTracks, methodClasses)
        print(len(workingMethodObjects), [wmo for wmo in workingMethodObjects])

        # runAllMethodsInSequence(workingMethodObjects)
        # for workingMethod in workingMethodObjects:
        #     self._printResultFiles(workingMethod, ['stderr', 'stdout', 'output'])

    def testGenometriCorr(self, chrLenFile, tracks):
        raise Exception('With current setup, too long running time to function as unit test')
        # method = GenometriCorr()
        # method.setQueryTrackFileNames([tracks[0]])
        # method.setReferenceTrackFileNames([tracks[1]])
        # method.setChromLenFileName(chrLenFile)
        # method.setManualParam('ecdfPermNum', 5)
        # method.setManualParam('meanPermNum', 5)
        # method.setManualParam('jaccardPermNum', 5)
        # runAllMethodsInSequence([method])
        # self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testStereoGene(self, chrLenFile, tracks):
        method = StereoGene()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(1, method)

    def testStereoGeneOneVsMulti(self, chrLenFile, tracks):
        refTracks = [tracks[2], tracks[3]]
        method = MultiMethod(StereoGene, [tracks[0]], refTracks)
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(len(refTracks), method)

    def testStereoGeneMultiVsMulti(self, chrLenFile, tracks):
        raise Exception('With current setup, too long running time to function as unit test')

        qTracks = [tracks[0], tracks[1]]
        refTracks = [tracks[2], tracks[3]]
        method = MultiMethod(StereoGene, qTracks, refTracks)
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(len(qTracks) * len(refTracks), method)

    def testIntervalStats(self, chrLenFile, tracks):
        method = IntervalStats()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('o', 'output')
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testIntervalStatsMultiOneVsMany(self, chrLenFile, tracks):
        method = MultiMethod(IntervalStats, [tracks[0]], [tracks[2], tracks[3]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('o', 'output')
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testIntervalStatsMultiManyVsMany(self, chrLenFile, tracks):
        method = MultiMethod(IntervalStats, [tracks[0], tracks[1]], [tracks[2], tracks[3]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('o', 'output')
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testGiggleDynamic(self, chrLenFile, tracks):
        method = Giggle()
        method.setQueryTrackFileNames([tracks[8]])
        refTracks = [tracks[13], tracks[11], tracks[12]]
        method.setReferenceTrackFileNames(refTracks)
        # method = MultiMethod(Giggle, [tracks[8]], refTracks)
        method.setChromLenFileName(chrLenFile)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(len(refTracks), method)

    def testGiggleReference(self, chrLenFile, tracks):
        method = Giggle()
        method.setQueryTrackFileNames([tracks[9]])
        method.setManualParam('trackIndex', 'LOLACore_170206')
        method.setManualParam('genome', 'hg19')
        method.setManualParam('trackCollection', 'codex')
        method.setChromLenFileName(chrLenFile)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testGiggleMultiManyVsMany(self, chrLenFile, tracks):
        refTracks = [tracks[11], tracks[12]]
        qTracks = [tracks[9], tracks[10]]
        method = MultiMethod(Giggle, qTracks, refTracks)
        method.setChromLenFileName(chrLenFile)
        runAllMethodsInSequence([method])
        expectedResulstNr = len(qTracks) * len(refTracks)
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(expectedResulstNr, method)

    def testLOLADynamic(self, chrLenFile, tracks):
        raise Exception('With current setup, too long running time to function as unit test')
        method = LOLA()
        method.setQueryTrackFileNames([tracks[8]])
        method.setReferenceTrackFileNames([tracks[2], tracks[3]])
        method.setRestrictedAnalysisUniverse(RestrictedThroughInclusion(tracks[0]))
        method.preserveClumping(False)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    # def testLOLAReference(self, chrLenFile, tracks):
    #     method = LOLA()
    #     method.setQueryTrackFileNames([tracks[8]])
    #     method.setRestrictedAnalysisUniverse(RestrictedThroughInclusion(tracks[0]))
    #     method.setManualParam('trackIndex', 'LOLACore_170206')
    #     method.setManualParam('genome', 'hg19')
    #     method.setManualParam('trackCollection', 'codex')
    #     method.preserveClumping(False)
    #     runAllMethodsInSequence([method])
    #     self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testGoShifter(self, chrLenFile, tracks):
        method = GoShifter()
        snpmap = pkg_resources.resource_filename('tests.resources', 'snpmap.tabular')
        annotation = pkg_resources.resource_filename('tests.resources', 'annotation.bed.gz')
        proxies = pkg_resources.resource_filename('tests.resources', 'proxies.txt')
        method.setManualParam('s', snpmap)
        method.setManualParam('a', annotation)
        method.setManualParam('i', proxies)
        method.setManualParam('p', 10)
        method.setManualParam('o', 'output')
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    @staticmethod
    def _getSampleFileName(contents):
        sampleFile = NamedTemporaryFile(mode='w+', dir='/tmp', suffix='.bed')
        sampleFile.write(contents)
        sampleFile.flush()
        return sampleFile

    @staticmethod
    def _printResultFiles(method, keys):
        if isinstance(method, MultiMethod):
            resultFilesDictList = method.getResultFilesDictList()
        else:
            resultFilesDictList = [method.getResultFilesDict()]

        for resultFilesDict in resultFilesDictList:
            for key in keys:
                assert key in resultFilesDict, (key,resultFilesDict)
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
