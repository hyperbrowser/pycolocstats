import os
from tempfile import NamedTemporaryFile

from conglomerate.methods.randomizer import Randomizer
from conglomerate.methods.adder import Adder
from conglomerate.methods.subtractor import Subtractor
from conglomerate.methods.genometricorr import GenometriCorr
from conglomerate.tools.runner import runAllMethodsInSequence


class TestMethods(object):
    def testRandomizer(self):
        track1, track2, chrlen = self._getSampleFiles()
        method = Randomizer(TRACK_1=track1.name,
                            TRACK_2=track2.name,
                            CHROM_LENGTHS=chrlen.name,
                            LOGICAL_ARG_1=10,
                            LOGICAL_ARG_2=6)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    def testAdder(self):
        track1, track2, chrlen = self._getSampleFiles()
        method = Adder(TRACK_1=track1.name,
                       TRACK_2=track2.name,
                       CHROM_LENGTHS=chrlen.name,
                       LOGICAL_ARG_1=4.0,
                       LOGICAL_ARG_2=2.0,
                       LOGICAL_ARG_3="add")
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    def testSubtractor(self):
        track1, track2, chrlen = self._getSampleFiles()
        method = Subtractor(TRACK_1=track1.name,
                            TRACK_2=track2.name,
                            CHROM_LENGTHS=chrlen.name,
                            LOGICAL_ARG_1=4.0,
                            LOGICAL_ARG_2=2.0,
                            LOGICAL_ARG_3="subtract")
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    def testGenometriCorr(self):
        track1, track2, chrlen = self._getSampleFiles()
        method = GenometriCorr(TRACK_1=track1.name,
                               TRACK_2=track2.name,
                               CHROM_LENGTHS=chrlen.name,
                               LOGICAL_ARG_1=4.0,
                               LOGICAL_ARG_2=2.0,
                               LOGICAL_ARG_3="subtract")
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    @staticmethod
    def _getSampleFiles():
        track1 = NamedTemporaryFile()
        track2 = NamedTemporaryFile()
        chrlen = NamedTemporaryFile()
        open(track1.name, 'w').write('Track 1 contents')
        open(track2.name, 'w').write('Track 2 contents')
        open(chrlen.name, 'w').write('Chromosome lengths contents')
        return track1, track2, chrlen

    @staticmethod
    def _printResultFiles(method, keys):
        for key in keys:
            print(key, '\n------\n', open(method.getResultFilesDict()[key]).read())

