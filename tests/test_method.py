import os
from tempfile import NamedTemporaryFile

from conglomerate.methods.randomizer import Randomizer
from conglomerate.methods.adder import Adder
from conglomerate.methods.subtractor import Subtractor
from conglomerate.tools.runner import runAllMethodsInSequence


class TestMethods(object):
    def testRandomizer(self):
        track1 = NamedTemporaryFile()
        track2 = NamedTemporaryFile()
        method = Randomizer(TRACK_1=track1.name,
                            TRACK_2=track2.name,
                            LOGICAL_ARG_1=10,
                            LOGICAL_ARG_2=6)
        runAllMethodsInSequence([method])
        print(track1.name)
        print(track2.name)
        self._printResultFiles(method, ['stderr', 'stdout'])

    def _printResultFiles(self, method, keys):
        for key in keys:
            print(key, '\n------\n', open(method.getResultFilesDict()[key]).read())

    def testAdder(self):
        track1 = NamedTemporaryFile()
        track2 = NamedTemporaryFile()
        method = Adder(TRACK_1=track1.name,
                       TRACK_2=track2.name,
                       LOGICAL_ARG_1=4.0,
                       LOGICAL_ARG_2=2.0,
                       LOGICAL_ARG_3="add")
        runAllMethodsInSequence([method])
        print(track1.name)
        print(track2.name)
        self._printResultFiles(method, ['stderr', 'stdout'])

    def testSubtractor(self):
        track1 = NamedTemporaryFile()
        track2 = NamedTemporaryFile()
        method = Adder(TRACK_1=track1.name,
                       TRACK_2=track2.name,
                       LOGICAL_ARG_1=4.0,
                       LOGICAL_ARG_2=2.0,
                       LOGICAL_ARG_3="subtract")
        runAllMethodsInSequence([method])
        print(track1.name)
        print(track2.name)
        self._printResultFiles(method, ['stderr', 'stdout'])
