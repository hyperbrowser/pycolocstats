from __future__ import absolute_import, division, print_function, unicode_literals

from future.utils import with_metaclass
from abc import ABCMeta, abstractmethod
from conglomerate.methods.interface import UniformInterface
# from conglomerate.methods.typecheck import takes
from conglomerate.tools.constants import CATCH_METHOD_EXCEPTIONS, VERBOSE_RUNNING
from conglomerate.tools.exceptions import MissingMandatoryParameters
from conglomerate.tools.job import Job
from conglomerate.tools.tool import Tool

__metaclass__ = type


class Method(UniformInterface):
    def __init__(self):
        self._params = self._getTool().createJobParamsDict()
        self._setDefaultParamValues()
        self._resultFilesDict = None
        self._ranSuccessfully = None
        self._errorMessage = None
        self._requiredFileCopies = {}
        self._trackTitleMappings = {}
        self._methodCls = self.__class__

    def _addTrackTitleMapping(self, path, title):
        self._trackTitleMappings[path] = title

    def getRemappedResultDict(self, resultDict):
        remappedDict = {}
        for origKey in resultDict:
            #assert all([k in self._trackTitleMappings for k in origKey]), (origKey, self._trackTitleMappings)
            remappedKey = tuple([self._trackTitleMappings[k] if k in self._trackTitleMappings else k
                                 for k in origKey])
            if VERBOSE_RUNNING:
                nonMapped = [k for k in origKey if not k in self._trackTitleMappings]
                if len(nonMapped)>0:
                    print('Not mapped track titles: ', nonMapped, 'based on mapping: ', self._trackTitleMappings)

            remappedDict[ remappedKey ] = resultDict[origKey]
        return remappedDict

    def _getTool(self):
        return Tool(self._getToolName())

    def setManualParam(self, key, val):
        """
        For setting tool parameters directly, without going through properties (like allowOverlaps)
        """
        self._params[key] = val

    def checkForAbsentMandatoryParameters(self):
        absentMandatoryParameters = self._params.getAbsentMandatoryParameters()
        if absentMandatoryParameters:
            raise MissingMandatoryParameters(absentMandatoryParameters)

    def createJobs(self):
        self.checkForAbsentMandatoryParameters()
        self.performRequiredFileCopying()
        return [Job(self._getTool(), self._params)]

    def setResultFilesDict(self, resultFilesDict):
        self._resultFilesDict = resultFilesDict
        self._ranSuccessfully = True #will stay True unless parseResultFiles manually sets to False or throws Exception
        try:
            self._parseResultFiles()
        except:
            self._ranSuccessfully = False
            if not CATCH_METHOD_EXCEPTIONS:
                raise

    def getResultFilesDict(self):
        return self._resultFilesDict

    def setRunSuccessStatus(self, status, errorMessage=None):
        self._ranSuccessfully = status
        if errorMessage is not None:
            self._errorMessage = errorMessage

    def ranSuccessfully(self):
        #Needs to be set to specific value before this method is called..
        assert hasattr(self, '_ranSuccessfully') and self._ranSuccessfully in [False, True], self._ranSuccessfully
        return self._ranSuccessfully

    def getErrorDetails(self):
        if self._errorMessage is None:
            return 'Error message parsing not implemented for this tool'
        else:
            return self._errorMessage

    def __repr__(self):
        return self.__class__.__name__

    def _getBedExtendedFileName(self, trackFn): #TODO: Replace with better handling of temporary files
        if trackFn.endswith('bed'):
            return trackFn
        from tempfile import mkdtemp
        import os
        #import shutil
        #bedPath = os.path.join(mkdtemp(), trackFn.replace('.dat','.bed'))
        #bedPath = '/data/tmp/congloTmp/adHocBed/' + os.path.basename(trackFn).replace('.dat','.bed')
        from conglomerate.tools.util import getTemporaryFileName
        bedPath = getTemporaryFileName()
        #shutil.copytree(src=trackFn, dst=bedFn,symlinks=True)
        #shutil.copy(src=trackFn, dst=bedPath)
        self._requiredFileCopies[trackFn] = bedPath
        return bedPath

    def performRequiredFileCopying(self):
        for src in self._requiredFileCopies:
            dst = self._requiredFileCopies[src]
            import shutil
            shutil.copy(src, dst)
    # def getRefTracksMappedToIndexParams(self, trackFnList):
    #     assert trackFnList not in [ ['dummy1', 'dummy2'] ]

class SingleQueryTrackMethodMixin(with_metaclass(ABCMeta, object)):
    def setQueryTrackFileNames(self, trackFnList):
        assert len(trackFnList) == 1
        self._setQueryTrackFileName(trackFnList[0])

    @abstractmethod
    def _setQueryTrackFileName(self, trackFn):
        pass


class SingleReferenceTrackMethodMixin(with_metaclass(ABCMeta, object)):
    def setReferenceTrackFileNames(self, trackFnList):
        assert len(trackFnList) == 1
        self._setReferenceTrackFileName(trackFnList[0])

    @abstractmethod
    def _setReferenceTrackFileName(self, trackFn):
        pass

    def setPredefinedTrackIndexAndCollection(self, trackIndex, trackCollection):
        pass


class MultipleQueryTracksMethodMixin(with_metaclass(ABCMeta, object)):
    def setQueryTrackFileNames(self, trackFnList):
        assert len(trackFnList) > 0
        self._setQueryTrackFileNames(trackFnList)

    @abstractmethod
    def _setQueryTrackFileNames(self, trackFnList):
        pass


class MultipleReferenceTracksMethodMixin(with_metaclass(ABCMeta, object)):
    def setReferenceTrackFileNames(self, trackFnList):
        assert len(trackFnList) > 0
        self._setReferenceTrackFileNames(trackFnList)

    @abstractmethod
    def _setReferenceTrackFileNames(self, trackFnList):
        pass

    def setPredefinedTrackIndexAndCollection(self, trackIndex, trackCollection):
        pass


class CollectionReferenceTracksMethodMixin(with_metaclass(ABCMeta, object)):
    def setReferenceTrackFileNames(self, trackFnList):
        assert len(trackFnList) == 0

    # @takes(str, str)
    def setPredefinedTrackIndexAndCollection(self, trackIndex, trackCollection):
        self._setPredefinedTrackIndexAndCollection(trackIndex, trackCollection)

    @abstractmethod
    def _setPredefinedTrackIndexAndCollection(self, trackIndex, trackCollection):
        pass


class OneVsOneMethod(SingleQueryTrackMethodMixin,
                     SingleReferenceTrackMethodMixin,
                     Method):
    pass


class OneVsManyMethod(SingleQueryTrackMethodMixin,
                      MultipleReferenceTracksMethodMixin,
                      Method):
    pass


class ManyVsManyMethod(MultipleQueryTracksMethodMixin,
                       MultipleReferenceTracksMethodMixin,
                       Method):
    pass


class OneVsCollectionMethod(SingleQueryTrackMethodMixin,
                            CollectionReferenceTracksMethodMixin,
                            Method):
    pass


class ManyVsCollectionsMethod(MultipleQueryTracksMethodMixin,
                              CollectionReferenceTracksMethodMixin,
                              Method):
    pass
