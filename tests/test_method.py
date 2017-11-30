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
from conglomerate.tools.runner import runAllMethodsInSequence


@pytest.fixture(scope='function')
def tracks():
    return [pkg_resources.resource_filename('tests.resources', 'H3K4me1_no_overlaps.bed'),
            pkg_resources.resource_filename('tests.resources', 'H3K4me3_no_overlaps.bed'),
            pkg_resources.resource_filename('tests.resources', 'H3K4me1_with_overlaps.bed'),
            pkg_resources.resource_filename('tests.resources', 'H3K4me3_with_overlaps.bed'),
            pkg_resources.resource_filename('tests.resources', 'H3K4me1_no_overlaps.bed.gz'),
            pkg_resources.resource_filename('tests.resources', 'H3K4me3_no_overlaps.bed.gz'),
            pkg_resources.resource_filename('tests.resources', 'H3K4me1_with_overlaps.bed.gz'),
            pkg_resources.resource_filename('tests.resources', 'H3K4me3_with_overlaps.bed.gz'),
            pkg_resources.resource_filename('tests.resources', 'H3K4me1_no_overlaps_cropped.bed'),
            pkg_resources.resource_filename('tests.resources', 'Refseq_Genes_cropped.bed.gz'),
            pkg_resources.resource_filename('tests.resources', 'Ensembl_Genes_cropped.bed.gz')]

@pytest.fixture(scope='function')
def chrLenFile():
    return pkg_resources.resource_filename('tests.resources', 'chrom_lengths.tabular')

@pytest.mark.usefixtures('chrLenFile', 'tracks')
class TestMethods(object):

    def testGenometriCorr(self, chrLenFile, tracks):
        method = GenometriCorr()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('ecdfPermNum', 5)
        method.setManualParam('meanPermNum', 5)
        method.setManualParam('jaccardPermNum', 5)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testStereoGene(self, chrLenFile, tracks):
        method = StereoGene()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        # method.setReferenceTrackFileNames([tracks[1],tracks[2],tracks[3]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        runAllMethodsInSequence([method])
        method._printResults()
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    @pytest.mark.skip
    def testIntervalStats(self, chrLenFile, tracks):
        method = IntervalStats()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('o', 'output')
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    @pytest.mark.skip
    def testIntervalStatsMultiOneVsMany(self, chrLenFile, tracks):
        method = MultiMethod(IntervalStats, [tracks[0]], [tracks[2], tracks[3]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('o', 'output')
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    @pytest.mark.skip
    def testIntervalStatsMultiManyVsMany(self, chrLenFile, tracks):
        method = MultiMethod(IntervalStats, [tracks[0], tracks[1]], [tracks[2], tracks[3]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('o', 'output')
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testGiggle(self, chrLenFile, tracks):
        method = Giggle()
        method.setQueryTrackFileNames([tracks[4]])
        refTracks = [tracks[5], tracks[9], tracks[10]]
        method.setReferenceTrackFileNames(refTracks)
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('index_o', 'index')
        method.setManualParam('search_i', 'index')

        runAllMethodsInSequence([method])
        assert len(refTracks) == len(method.getParsedFullResults().getResults()), \
            "Expected %i results got %i" % (len(refTracks), len(method.getParsedFullResults().getResults()))
        assert len(refTracks) == len(method.getTestStatistic()), \
            "Expected %i test statistic results got %i" % (len(refTracks), len(method.getTestStatistic()))
        assert len(refTracks) == len(method.getPValue()), \
            "Expected %i p-values got %i" % (len(refTracks), len(method.getPValue()))
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testGiggleMultiManyVsMany(self, chrLenFile, tracks):
        refTracks = [tracks[9], tracks[10]]
        method = MultiMethod(Giggle, [tracks[4], tracks[5]], refTracks)
        method.setManualParam('index_o', 'index')
        method.setManualParam('search_i', 'index')
        method.setChromLenFileName(chrLenFile)
        # method.setManualParam('search_s', True)
        # method.setManualParam('search_v', True)
        # method.setManualParam('search_l', True)
        runAllMethodsInSequence([method])
        assert len(refTracks) == len(method.getParsedFullResults().getResults()), \
            "Expected %i results got %i" % (len(refTracks), len(method.getParsedFullResults().getResults()))
        assert len(refTracks) == len(method.getTestStatistic()), \
            "Expected %i test statistic results got %i" % (len(refTracks), len(method.getTestStatistic()))
        assert len(refTracks) == len(method.getPValue()), \
            "Expected %i p-values got %i" % (len(refTracks), len(method.getPValue()))
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testLOLA(self, chrLenFile, tracks):
        method = LOLA()
        method.setQueryTrackFileNames([tracks[8]])
        method.setReferenceTrackFileNames([tracks[2],tracks[3]])
        method.setRestrictedAnalysisUniverse(RestrictedThroughInclusion(tracks[0]))
        method.preserveClumping(False)
        # method.setManualParam('userset', tracks[8])
        # method.setManualParam('useruniverse', tracks[0])
        # method.setManualParam('regiondb', [tracks[2], tracks[3]])
        runAllMethodsInSequence([method])
        # commenting this out, because this breaks tests:
        # print('TEMP1: ', (method.getPValue()))
        # print('TEMP2: ', (method.getTestStatistic()))
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

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
                print(key)
                print('------')
                print('Local path: ' + resultFilesDict[key])
                print('------')
                print('\n'.join(os.listdir(resultFilesDict[key])) if key == 'output'
                      else open(resultFilesDict[key]).read())
