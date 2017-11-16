from conglomerate.methods.method import Method
from conglomerate.tools.tool import GEOMETRICORR_TOOL


class GeometriCorr(Method):
    def _getMappings(self):
        return {'TRACK_1': 't1',
                'TRACK_2': 't2',
                'LOGICAL_ARG_1': 'a',
                'LOGICAL_ARG_2': 'b',
                'LOGICAL_ARG_3': 'operation'}

    def _getTool(self):
        return GEOMETRICORR_TOOL
