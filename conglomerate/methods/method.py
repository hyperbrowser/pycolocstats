from abc import ABCMeta, abstractmethod
import yaml
import cwltool.factory


class Method:
    __metaclass__ = ABCMeta

    PROPERTIES = ["LOGICAL_ARG_1", "LOGICAL_ARG_2", "LOGICAL_ARG_3"]

    cwltool_factory = cwltool.factory.Factory()

    def run(self, **properties):
        tool = Method.cwltool_factory.make(self.__get_tool_path__())
        tool.factory.execkwargs["use_container"] = True
        mapped_params = self.__map_params__(**properties)
        return tool(**mapped_params)

    def __get_tool_path__(self):
        return "../../tools/%s/tool.cwl" % self.__get_tool_name__()

    def __read_inputs__(self):
        with open(self.__get_tool_path__(), 'r') as stream:
            try:
                return yaml.load(stream)["inputs"]
            except yaml.YAMLError as exc:
                print(exc)

    def __map_params__(self, **properties):
        inputs = [i["id"] for i in self.__read_inputs__()]
        mapped_properties = {}
        for key, value in self.__get_mappings__().items():
            assert key in Method.PROPERTIES
            assert value in inputs
            mapped_properties[self.__get_mappings__()[key]] = properties[key]
        return mapped_properties

    @abstractmethod
    def __get_mappings__(self):
        pass

    @abstractmethod
    def __get_tool_name__(self):
        pass
