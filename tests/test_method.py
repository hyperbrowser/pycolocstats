from tempfile import NamedTemporaryFile

from conglomerate.methods.randomizer import Randomizer
from conglomerate.methods.adder import Adder
from conglomerate.methods.subtractor import Subtractor
from conglomerate.tools.job import JobRunner


class TestMethods(object):
    # def testRandomizer(self):
    #     method = Randomizer()
    #     job = method.createJob(LOGICAL_ARG_1=10, LOGICAL_ARG_2=6)
    #     results = JobRunner.runJobs([job])
    #     print(results)

    # def testRandomizer(self):
    #     method = Randomizer()
    #     method.setLogicalArg1(10)
    #     method.setLogicalArg2(6)
    #     job = method.createJob()
    #     results = JobRunner.runJobs([job])
    #     print(results)

    def testAdder(self):
        method = Adder()
        track1 = NamedTemporaryFile()
        track2 = NamedTemporaryFile()
        job = method.createJob(TRACK_1={'class': 'File', 'location': 'file://' + track1.name},
                               TRACK_2={'class': 'File', 'location': 'file://' + track2.name},
                               LOGICAL_ARG_1=4.0,
                               LOGICAL_ARG_2=2.0,
                               LOGICAL_ARG_3="add")
        results = JobRunner.runJobs([job])
        print(track1.name)
        print(track2.name)
        print(results)

    # def testSubtractor(self):
    #     method = Subtractor()
    #     job = method.createJob(LOGICAL_ARG_1=4.0, LOGICAL_ARG_2=2.0, LOGICAL_ARG_3="subtract")
    #     results = JobRunner.runJobs([job])
    #     print(results)
