from conglomerate.methods.method import Method


class Adder(Method):
    def _getMappings(self):
        return {"LOGICAL_ARG_1": "a", "LOGICAL_ARG_2": "b", "LOGICAL_ARG_3": "operation"}

    def _getToolName(self):
        return "calculator"
