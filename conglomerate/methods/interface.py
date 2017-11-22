from abc import ABCMeta, abstractmethod


class ColocMeasure:
    pass


class ColocMeasureOverlap:
    #@takes("ColocMeasureOverlap", bool, bool)
    def __init__(self, includeFlanks, countWholeIntervals):
        self._includeFlanks = includeFlanks
        self._countWholeIntervals = countWholeIntervals

class ColocMeasureProximity(ColocMeasureOverlap):
    pass

class ColocMeasureCorrelation(ColocMeasureOverlap):
    pass

class RestrictedAnalysisUniverse:
    pass

class RestrictedThroughInclusion(RestrictedAnalysisUniverse):
    def __init__(self, path):
        pass

class RestrictedThroughExclusion(RestrictedAnalysisUniverse):
    pass

class RestrictedThroughPreDefined(RestrictedAnalysisUniverse):
    pass


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
    #@takes("UniformInterface", ColocMeasure)
    def setColocMeasure(self, colocMeasure):
        pass

    #@takes("UniformInterface", any(None,RestrictedAnalysisUniverse))
    @abstractmethod
    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        pass

    @abstractmethod
    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        ""
        # assert preservationScheme in [PRESERVE_HETEROGENEITY_NOT, PRESERVE_HETEROGENEITY_AS_NEIGHBORHOOD, PRESERVE_HETEROGENEITY_WITHIN_SUPPLIED_REGIONS]
        # if preservationScheme==PRESERVE_HETEROGENEITY_WITHIN_SUPPLIED_REGIONS:
        #     assert fn is not None
        pass

    PRESERVE_HETEROGENEITY_NOT = '...'
    PRESERVE_HETEROGENEITY_AS_NEIGHBORHOOD = '...'
    PRESERVE_HETEROGENEITY_WITHIN_SUPPLIED_REGIONS = '...'

    @abstractmethod
    # @takes("UniformInterface", bool)
    def preserveClumping(self, preserve):
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
