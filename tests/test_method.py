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


class TestMethods(object):
    def testGenometriCorr(self):
        track1, track2, track3, track4, chrlen, track5, track6, track7, track8, track9, track10, track11 = self._getSampleFileNames()
        method = GenometriCorr()
        method.setQueryTrackFileNames([track1])
        method.setReferenceTrackFileNames([track2])
        method.setChromLenFileName(chrlen)
        method.setManualParam('ecdfPermNum', 5)
        method.setManualParam('meanPermNum', 5)
        method.setManualParam('jaccardPermNum', 5)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testStereoGene(self):
        track1, track2, track3, track4, chrlen, track5, track6, track7, track8, track9, track10, track11 = self._getSampleFileNames()
        method = StereoGene()
        method.setQueryTrackFileNames([track1])
        method.setReferenceTrackFileNames([track2])
        # method.setReferenceTrackFileNames([track2,track3,track4])
        method.setChromLenFileName(chrlen)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        runAllMethodsInSequence([method])
        method._printResults()
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testIntervalStats(self):
        track1, track2, track3, track4, chrlen, track5, track6, track7, track8, track9, track10, track11 = self._getSampleFileNames()
        method = IntervalStats()
        method.setQueryTrackFileNames([track1])
        method.setReferenceTrackFileNames([track2])
        method.setChromLenFileName(chrlen)
        method.setManualParam('o', 'output')
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testIntervalStatsMultiOneVsMany(self):
        track1, track2, track3, track4, chrlen, track5, track6, track7, track8, track9, track10, track11 = self._getSampleFileNames()
        method = MultiMethod(IntervalStats, [track1], [track3, track4])
        method.setChromLenFileName(chrlen)
        method.setManualParam('o', 'output')
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testIntervalStatsMultiManyVsMany(self):
        track1, track2, track3, track4, chrlen, track5, track6, track7, track8, track9, track10, track11 = self._getSampleFileNames()
        method = MultiMethod(IntervalStats, [track1, track2], [track3, track4])
        method.setChromLenFileName(chrlen)
        method.setManualParam('o', 'output')
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testGiggle(self):
        track1, track2, track3, track4, chrlen, track5, track6, track7, track8, track9, track10, track11 = self._getSampleFileNames()
        method = Giggle()
        method.setQueryTrackFileNames([track5])
        refTracks = [track6, track10, track11]
        method.setReferenceTrackFileNames(refTracks)
        method.setChromLenFileName(chrlen)
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

    def testGiggleMultiManyVsMany(self):
        track1, track2, track3, track4, chrlen, track5, track6, track7, track8, track9, track10, track11 = self._getSampleFileNames()
        refTracks = [track10, track11]
        method = MultiMethod(Giggle, [track5, track6], refTracks)
        method.setManualParam('index_o', 'index')
        method.setManualParam('search_i', 'index')
        method.setChromLenFileName(chrlen)
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

    def testLOLA(self):
        track1, track2, track3, track4, chrlen, track5, track6, track7, track8, track9, track10, track11 = self._getSampleFileNames()
        method = LOLA()
        method.setQueryTrackFileNames([track9])
        method.setReferenceTrackFileNames([track3,track4])
        method.setRestrictedAnalysisUniverse(RestrictedThroughInclusion(track1))
        method.preserveClumping(False)
        # method.setManualParam('userset', track9)
        # method.setManualParam('useruniverse', track1)
        # method.setManualParam('regiondb', [track3, track4])
        runAllMethodsInSequence([method])
        # commenting this out, because this breaks tests:
        # print('TEMP1: ', (method.getPValue()))
        # print('TEMP2: ', (method.getTestStatistic()))
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])

    def testGoShifter(self):
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
    def _getSampleFileNames():
        track1 = pkg_resources.resource_filename('tests.resources', 'H3K4me1_no_overlaps.bed')
        track2 = pkg_resources.resource_filename('tests.resources', 'H3K4me3_no_overlaps.bed')
        track3 = pkg_resources.resource_filename('tests.resources', 'H3K4me1_with_overlaps.bed')
        track4 = pkg_resources.resource_filename('tests.resources', 'H3K4me3_with_overlaps.bed')
        chrlen = pkg_resources.resource_filename('tests.resources', 'chrom_lengths.tabular')
        track5 = pkg_resources.resource_filename('tests.resources', 'H3K4me1_no_overlaps.bed.gz')
        track6 = pkg_resources.resource_filename('tests.resources', 'H3K4me3_no_overlaps.bed.gz')
        track7 = pkg_resources.resource_filename('tests.resources', 'H3K4me1_with_overlaps.bed.gz')
        track8 = pkg_resources.resource_filename('tests.resources', 'H3K4me3_with_overlaps.bed.gz')
        track9 = pkg_resources.resource_filename('tests.resources', 'H3K4me1_no_overlaps_cropped.bed')
        track10 = pkg_resources.resource_filename('tests.resources', 'Refseq_Genes_cropped.bed.gz')
        track11 = pkg_resources.resource_filename('tests.resources', 'Ensembl_Genes_cropped.bed.gz')
        return track1, track2, track3, track4, chrlen, track5, track6, track7, track8, track9, track10, track11

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
