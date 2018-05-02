from __future__ import absolute_import, division, print_function, unicode_literals


from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass, python_2_unicode_compatible
# from pycolocstats.methods.typecheck import takes, one_of

__metaclass__ = type

class InvalidSpecification(object):
    def __init__(self, reason):
        self._reason = reason

    def __str__(self):
        return 'Invalid specificaiton, due to: ' + self._reason

class ColocMeasure(with_metaclass(ABCMeta, object)):
    pass


@python_2_unicode_compatible
class ColocMeasureOverlap(ColocMeasure):
    # @takes("ColocMeasureOverlap", bool, bool, int, int)
    def __init__(self, includeFlanks, countWholeIntervals, flankSizeUpstream=None, flankSizeDownstream=None):
        self._includeFlanks = includeFlanks
        self._countWholeIntervals = countWholeIntervals
        self._flankSizeUpstream = flankSizeUpstream
        self._flankSizeDownstream = flankSizeDownstream

    def __str__(self):
        return u'Overlap'


@python_2_unicode_compatible
class ColocMeasureProximity(ColocMeasure):
    # @takes("ColocMeasureProximity", one_of('start','midpoint','end','closest'), bool)
    def __init__(self, proximityAnchor, isGeometricDistance):
        self._proximityAnchor = proximityAnchor
        self._isGeometricDistance = isGeometricDistance

    def __str__(self):
        return u'Proximity (Geometric distance)' if self._isGeometricDistance else u'Proximity'


@python_2_unicode_compatible
class ColocMeasureCorrelation(ColocMeasure):
    # @takes("ColocMeasureCorrelation", one_of('genome-wide', 'fine-scale', 'local'))
    def __init__(self, typeOfCorrelation):
        self._typeOfCorrelation = typeOfCorrelation

    def __str__(self):
        return  u'Correlation ({})'.format(self._typeOfCorrelation) if self._typeOfCorrelation else u'Correlation'


class RestrictedAnalysisUniverse(with_metaclass(ABCMeta, object)):
    def __repr__(self):
        return self.__class__.__name__ + '(' + str(self.trackFile) + ')'


@python_2_unicode_compatible
class RestrictedThroughInclusion(RestrictedAnalysisUniverse):
    def __init__(self, trackFile):
        self.trackFile = trackFile

    def __str__(self):
        return u'Restricted regions (use regions from track)'


@python_2_unicode_compatible
class RestrictedThroughExclusion(RestrictedAnalysisUniverse):
    def __init__(self, path):
        pass

    def __str__(self):
        return u'Restricted regions (exclude regions from track)'


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
        if preservationScheme != self.PRESERVE_HETEROGENEITY_NOT:
            self.setNotCompatible()

    PRESERVE_HETEROGENEITY_NOT = 'Distribute genomic elements across all analysis regions'
    PRESERVE_HETEROGENEITY_AS_NEIGHBORHOOD = 'Distribute each genomic element within a fixed size neighbourhood'
    PRESERVE_HETEROGENEITY_WITHIN_SUPPLIED_REGIONS = 'Distribute genomic elements within their original analysis regions'

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

    #@abstractmethod
    @classmethod
    def getTestStatDescr(cls):
        return 'not defined'

    @abstractmethod
    def getFullResults(self):
        """
        :return: Full result output as a string
        """
        pass

    def setRuntimeMode(self, mode):
        assert mode in ['quick', 'medium', 'accurate']
