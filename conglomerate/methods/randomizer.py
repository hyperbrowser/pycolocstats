from conglomerate.methods.method import Method
from tools.jobrunner import RANDOMIZER_TOOL


class Randomizer(Method):
    def _getMappings(self):
        return {"LOGICAL_ARG_1": "n", "LOGICAL_ARG_2": "max"}

    def _getTool(self):
        return RANDOMIZER_TOOL
