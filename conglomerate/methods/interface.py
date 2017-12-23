from __future__ import absolute_import, division, print_function, unicode_literals

from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass
# from conglomerate.methods.typecheck import takes, one_of

__metaclass__ = type

class InvalidSpecification(object):
    def __init__(self, reason):
        self._reason = reason

    def __str__(self):
        return 'Invalid specificaiton, due to: ' + self._reason

class ColocMeasure(with_metaclass(ABCMeta, object)):
    pass


class ColocMeasureOverlap(ColocMeasure):
    # @takes("ColocMeasureOverlap", bool, bool, int, int)
    def __init__(self, includeFlanks, countWholeIntervals, flankSizeUpstream=None, flankSizeDownstream=None):
        self._includeFlanks = includeFlanks
        self._countWholeIntervals = countWholeIntervals
        self._flankSizeUpstream = flankSizeUpstream
        self._flankSizeDownstream = flankSizeDownstream


class ColocMeasureProximity(ColocMeasure):
    # @takes("ColocMeasureProximity", one_of('start','midpoint','end','closest'), bool)
    def __init__(self, proximityAnchor, isGeometricDistance):
        self._proximityAnchor = proximityAnchor
        self._isGeometricDistance = isGeometricDistance


class ColocMeasureCorrelation(ColocMeasure):
    # @takes("ColocMeasureCorrelation", one_of('genome-wide', 'fine-scale', 'local'))
    def __init__(self, typeOfCorrelation):
        self._typeOfCorrelation = typeOfCorrelation


class RestrictedAnalysisUniverse(with_metaclass(ABCMeta, object)):
    pass


class RestrictedThroughInclusion(RestrictedAnalysisUniverse):
    def __init__(self, path):
        self.path = path


class RestrictedThroughExclusion(RestrictedAnalysisUniverse):
    def __init__(self, path):
        pass


class RestrictedThroughPreDefined(RestrictedAnalysisUniverse):
    def __init__(self, path):
        pass


class ConfounderHandlerSpec(with_metaclass(ABCMeta, object)):
    pass


class ConfounderHandlerPoisson(ConfounderHandlerSpec):
    def __init__(self, intensityFn):
        pass


class ConfounderHandlerPartialCorrelation(ConfounderHandlerSpec):
    def __init__(self, confounderFn):
        pass


class ConfounderHandlerStratifiedSampling(ConfounderHandlerSpec):
    pass


class UniformInterface(with_metaclass(ABCMeta, object)):
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
    def setGenomeName(self, genomeName):
        pass

    @abstractmethod
    def setChromLenFileName(self, chrLenFn):
        pass

    @abstractmethod
    def setQueryTrackFileNames(self, trackFnList):
        """
        For pairwise analysis or one-against-many analysis, this would be a list of one filename
        """
        pass

    @abstractmethod
    def setReferenceTrackFileNames(self, trackFnList):
        """
        For pairwise analysis, this would be a list of one filename
        """
        pass

    @abstractmethod
    # @takes(str, str)
    def setPredefinedTrackIndexAndCollection(self, trackIndex, trackCollection):
        pass

    @abstractmethod
    def setChromLenFileName(self, chromLenFile):
        pass

    @abstractmethod
    def setAllowOverlaps(self, allowOverlaps):
        pass

    @abstractmethod
    # @takes("UniformInterface", ColocMeasure)
    def setColocMeasure(self, colocMeasure):
        pass

    @abstractmethod
    ## @takes("UniformInterface", any([None, RestrictedAnalysisUniverse]))
    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        pass

    @abstractmethod
    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
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
