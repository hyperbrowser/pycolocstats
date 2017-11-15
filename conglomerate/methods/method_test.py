import unittest
from conglomerate.methods.randomizer import Randomizer
from conglomerate.methods.adder import Adder
from conglomerate.methods.subtractor import Subtractor


class MethodTests(unittest.TestCase):
    def test_randomizer(self):
        method = Randomizer()
        result = method.run(LOGICAL_ARG_1=10, LOGICAL_ARG_2=6)
        print(result)

    def test_adder(self):
        method = Adder()
        result = method.run(LOGICAL_ARG_1=4, LOGICAL_ARG_2=2, LOGICAL_ARG_3="add")
        print(result)

    def test_subtractor(self):
        method = Subtractor()
        result = method.run(LOGICAL_ARG_1=4, LOGICAL_ARG_2=2, LOGICAL_ARG_3="subtract")
        print(result)


if __name__ == "__main__":
    unittest.main()
