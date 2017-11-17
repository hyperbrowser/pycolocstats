import os
from tempfile import NamedTemporaryFile

from conglomerate.methods.mock.randomizer import Randomizer
from conglomerate.methods.mock.calculator import Adder
from conglomerate.methods.mock.calculator import Subtractor
from conglomerate.methods.genometricorr.genometricorr import GenometriCorr
from conglomerate.tools.runner import runAllMethodsInSequence


class TestMethods(object):
    def testAdder(self):
        method = Adder()
        method.setManualParam('a', 4.0)
        method.setManualParam('b', 2.0)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    def testSubtractor(self):
        method = Subtractor()
        method.setManualParam('a', 4.0)
        method.setManualParam('b', 2.0)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    def testRandomizer(self):
        chrlen = self._getSampleFiles()[2]
        method = Randomizer()
        method.setChromLenFileName(chrlen.name)
        method.setManualParam('max', 10)
        method.setManualParam('n', 6)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    def testGenometriCorr(self):
        track1, track2, chrlen = self._getSampleFiles()
        method = GenometriCorr()
        method.setTrackFileNames([track1.name, track2.name])
        method.setChromLenFileName(chrlen.name)
        method.setManualParam('a', 4.0)
        method.setManualParam('b', 2.0)
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

