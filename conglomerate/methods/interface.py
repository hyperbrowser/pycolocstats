from abc import ABCMeta, abstractmethod


class UniformInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _getToolName(self):
        """
        :return: Name of the tool as specified as constants in tools/tool.py. Refers to the
         directory name under the 'cwl' directory.
        """
        pass

    @abstractmethod
    def _setDefaultParamValues(self):
        """
        Sets default values for parameters that:
         1) are mandatory, or
         2) where the required default value is different than the default value defined by the
         tool (if the param is not specified).
        """
        pass

    @abstractmethod
    def setTrackFileNames(self, trackFileList):
        pass

    @abstractmethod
    def setChromLenFileName(self, chromLenFile):
        pass

    @abstractmethod
    def setAllowOverlaps(self, allowOverlaps):
        pass

    @abstractmethod
    def _parseResultFiles(self):
        pass

    @abstractmethod
    def getPValue(self):
        pass

    @abstractmethod
    def getTestStatistic(self):
        pass

    @abstractmethod
    def getFullResults(self):
        """
        :return: Full result output as a string
        """
        pass
