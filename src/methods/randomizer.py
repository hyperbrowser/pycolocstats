from src.methods import Method


class Randomizer(Method):
    def __get_mappings__(self):
        return {"LOGICAL_ARG_1": "n", "LOGICAL_ARG_2": "max"}

    def __get_tool_name__(self):
        return "randomizer"
