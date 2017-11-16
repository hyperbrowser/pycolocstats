from conglomerate.methods.method import Method
from conglomerate.tools.tool import RANDOMIZER_TOOL


class Randomizer(Method):
    def _getMappings(self):
        return {'TRACK_1': 't1',
                'TRACK_2': 't2',
                'CHROM_LENGTHS': 'chrlen',
                'LOGICAL_ARG_1': 'n',
                'LOGICAL_ARG_2': 'max'}

    def _getTool(self):
        return RANDOMIZER_TOOL
