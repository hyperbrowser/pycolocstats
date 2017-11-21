from tempfile import NamedTemporaryFile

import pkg_resources

from conglomerate.methods.genometricorr.genometricorr import GenometriCorr
from conglomerate.methods.intervalstats.intervalstats import IntervalStats
from conglomerate.methods.stereogene.stereogene import StereoGene
from conglomerate.tools.runner import runAllMethodsInSequence


class TestMethods(object):
    def testGenometriCorr(self):
        track1, track2, chrlen = self._getSampleFileNames()
        method = GenometriCorr()
        method.setTrackFileNames([track1, track2])
        method.setChromLenFileName(chrlen)
        method.setManualParam('t1Format', 'bed')
        method.setManualParam('t2Format', 'bed')
        method.setManualParam('ecdfPermNum', 5)
        method.setManualParam('meanPermNum', 5)
        method.setManualParam('jaccardPermNum', 5)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    def testStereoGene(self):
        track1, track2, chrlen = self._getSampleFileNames()
        method = StereoGene()
        method.setTrackFileNames([track1, track2])
        method.setChromLenFileName(chrlen)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    def testIntervalStats(self):
        track1, track2, chrlen = self._getSampleFileNames()
        method = IntervalStats()
        method.setTrackFileNames([track1, track2])
        method.setChromLenFileName(chrlen)
        method.setManualParam('o', 'output')
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    @staticmethod
    def _getSampleFileNames():
        track1 = pkg_resources.resource_filename('tests.resources', 'H3K4me1_no_overlaps.bed')
        track2 = pkg_resources.resource_filename('tests.resources', 'H3K4me3_no_overlaps.bed')
        chrlen = pkg_resources.resource_filename('tests.resources', 'chrom_lengths.tabular')
        return track1, track2, chrlen

    @staticmethod
    def _getSampleFileName(contents):
        sampleFile = NamedTemporaryFile(mode='w+', dir='/tmp', suffix='.bed')
        sampleFile.write(contents)
        sampleFile.flush()
        return sampleFile

    @staticmethod
    def _printResultFiles(method, keys):
        for key in keys:
            print(key, '\n------\n', open(method.getResultFilesDict()[key]).read())
