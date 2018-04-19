import os
import pkg_resources
import pytest

from pycolocstats.methods.interface import RestrictedAnalysisUniverse, RestrictedThroughInclusion
from pycolocstats.methods.lola.lola import LOLA
from pycolocstats.tools.WorkingMethodObjectParser import WorkingMethodObjectParser

from pycolocstats.core.types import TrackFile
from pycolocstats.methods.genometricorr.genometricorr import GenometriCorr
from pycolocstats.methods.giggle.giggle import Giggle
from pycolocstats.methods.multimethod import MultiMethod
from pycolocstats.methods.stereogene.stereogene import StereoGene
from pycolocstats.tools.WorkingMethodObjectParser import ALL_CONGLOMERATE_METHOD_CLASSES
from pycolocstats.tools.runner import runAllMethodsInSequence
from tests.test_method import TestMethodsBase

PRINT_RESULT_FILES = True
PRINT_TEST_STATISTICS = True

@pytest.fixture(scope='function')
def tracks():
    return [
            TrackFile(pkg_resources.resource_filename('pycolocstats', '../../tests/resources/test_track1.bed'), 't1'),
            TrackFile(pkg_resources.resource_filename('pycolocstats', '../../tests/resources/test_track2.bed'), 't2'),
            TrackFile(pkg_resources.resource_filename('pycolocstats', '../../tests/resources/test_track3.bed'), 't3'),
            TrackFile(pkg_resources.resource_filename('pycolocstats', '../../tests/resources/test_track4.bed'), 't4'),
            ]


@pytest.fixture(scope='function')
def chrLenFile():
    return pkg_resources.resource_filename('pycolocstats', '../../tests/resources/test_chrom_lengths_2.tabular')

@pytest.fixture(scope='function')
@pytest.mark.usefixtures('tracks')
def queryTrack(tracks):
    return tracks[0:1]

@pytest.fixture(scope='function')
@pytest.mark.usefixtures('tracks')
def refTracks(tracks):
    return tracks[1:2]

@pytest.mark.usefixtures('chrLenFile', 'tracks', 'queryTrack', 'refTracks')
class TestMethods(TestMethodsBase):
    def test_default_giggle(self, chrLenFile, queryTrack, refTracks):
        selectionValues = [[('setGenomeName', u'hg19')], [('setRestrictedAnalysisUniverse', None)],[('setRuntimeMode', u'quick')]]
        selectionValues.append([('setChromLenFileName',chrLenFile)])
        methodClasses = [Giggle]
        self._checkThatRuns(queryTrack, refTracks, selectionValues, methodClasses)


    def test_default_intervalStats(self, chrLenFile, queryTrack, refTracks):
        selectionValues = [[('setGenomeName', u'hg19')], [('setRestrictedAnalysisUniverse', None)],[('setRuntimeMode', u'quick')]]
        selectionValues.append([('setChromLenFileName',chrLenFile)])
        methodClasses = [Giggle]
        self._checkThatRuns(queryTrack, refTracks, selectionValues, methodClasses)

    def test_defaultWithBg_Lola(self, chrLenFile, queryTrack, refTracks, tracks):
        selectionValues = [[('setGenomeName', u'hg19')], [('setRestrictedAnalysisUniverse', RestrictedThroughInclusion(tracks[3]))], [('setRuntimeMode', u'quick')]]
        selectionValues.append([('setChromLenFileName',chrLenFile)])
        methodClasses = [LOLA]
        self._checkThatRuns(queryTrack, refTracks, selectionValues, methodClasses)

    # def test_default_genometriCorr(self, chrLenFile, queryTrack, refTracks):
    #     selectionValues = [[('setGenomeName', u'hg19')], [('setRestrictedAnalysisUniverse', None)],[('setRuntimeMode', u'quick')]]
    #     selectionValues.append([('setChromLenFileName',chrLenFile)])
    #     methodClasses = [GenometriCorr]
    #     self._checkThatRuns(queryTrack, refTracks, selectionValues, methodClasses)

    def _checkThatRuns(self, queryTrack, refTracks, selectionValues, methodClasses):
        workingMethodObjects = WorkingMethodObjectParser(queryTrack, refTracks, selectionValues, methodClasses).getWorkingMethodObjects()
        runAllMethodsInSequence(workingMethodObjects)
        for wmo in workingMethodObjects:
            if PRINT_RESULT_FILES:
                self._printResultFiles(wmo, ['stderr', 'stdout', 'output'])

            testStat = wmo.getTestStatistic()
            pval = wmo.getPValue()
            if PRINT_TEST_STATISTICS:
                print('TestStat ', wmo.getMethodName(), ': ', testStat)
            # self._assertMethodResultsSize(1, wmo)

