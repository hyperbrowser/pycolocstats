from src.methods import Method


class Adder(Method):
    def __get_mappings__(self):
        return {"LOGICAL_ARG_1": "a", "LOGICAL_ARG_2": "b", "LOGICAL_ARG_3": "operation"}

    def __get_tool_name__(self):
        return "calculator"
