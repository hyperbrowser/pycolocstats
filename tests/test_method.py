import os
from tempfile import NamedTemporaryFile, mkstemp

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
        chrlen = self._getSampleFileNames()[2]
        method = Randomizer()
        method.setChromLenFileName(chrlen.name)
        method.setManualParam('max', 10)
        method.setManualParam('n', 6)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    def testGenometriCorr(self):
        track1, track2, chrlen = self._getSampleFileNames()
        method = GenometriCorr()
        method.setTrackFileNames([track1.name, track2.name])
        method.setChromLenFileName(chrlen.name)
        method.setManualParam('a', 4.0)
        method.setManualParam('b', 2.0)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    @staticmethod
    def _getSampleFileNames():
        track1 = TestMethods._getSampleFileName('Track 1 contents\n')
        track2 = TestMethods._getSampleFileName('Track 2 contents\n')
        chrlen = TestMethods._getSampleFileName('Chromosome lengths contents\n')
        return track1, track2, chrlen

    @staticmethod
    def _getSampleFileName(contents):
        sampleFile = NamedTemporaryFile(mode='w+', dir='/tmp')
        sampleFile.write(contents)
        sampleFile.flush()
        return sampleFile

    @staticmethod
    def _printResultFiles(method, keys):
        for key in keys:
            print(key, '\n------\n', open(method.getResultFilesDict()[key]).read())

