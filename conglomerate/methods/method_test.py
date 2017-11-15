from conglomerate.methods.randomizer import Randomizer
from conglomerate.methods.adder import Adder
from conglomerate.methods.subtractor import Subtractor


class TestMethods(object):
    def testRandomizer(self):
        method = Randomizer()
        result = method.run(LOGICAL_ARG_1=10, LOGICAL_ARG_2=6)
        print(result)

    def testAdder(self):
        method = Adder()
        result = method.run(LOGICAL_ARG_1=4, LOGICAL_ARG_2=2, LOGICAL_ARG_3="add")
        print(result)

    def testSubtractor(self):
        method = Subtractor()
        result = method.run(LOGICAL_ARG_1=4, LOGICAL_ARG_2=2, LOGICAL_ARG_3="subtract")
        print(result)
