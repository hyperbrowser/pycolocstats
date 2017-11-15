from conglomerate.methods.randomizer import Randomizer
from conglomerate.methods.adder import Adder
from conglomerate.methods.subtractor import Subtractor
from tools.jobrunner import JobRunner


class TestMethods(object):
    def testRandomizer(self):
        method = Randomizer()
        job = method.createJob(LOGICAL_ARG_1=10, LOGICAL_ARG_2=6)
        results = JobRunner.runJobs([job])
        print(results)

    def testAdder(self):
        method = Adder()
        job = method.createJob(LOGICAL_ARG_1=4.0, LOGICAL_ARG_2=2.0, LOGICAL_ARG_3="add")
        results = JobRunner.runJobs([job])
        print(results)

    def testSubtractor(self):
        method = Subtractor()
        job = method.createJob(LOGICAL_ARG_1=4.0, LOGICAL_ARG_2=2.0, LOGICAL_ARG_3="subtract")
        results = JobRunner.runJobs([job])
        print(results)
