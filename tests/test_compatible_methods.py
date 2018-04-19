import pkg_resources
import pytest

from pycolocstats.methods.goshifter.goshifter import GoShifter
from pycolocstats.methods.interface import RestrictedThroughInclusion, ColocMeasureProximity
from pycolocstats.tools.WorkingMethodObjectParser import WorkingMethodObjectParser

from pycolocstats.core.types import TrackFile
from pycolocstats.methods.stereogene.stereogene import StereoGene
from pycolocstats.tools.WorkingMethodObjectParser import ALL_PYCOLOCSTATS_METHOD_CLASSES
from tests.test_method import TestMethodsBase

PRINT_RESULT_FILES = True
PRINT_TEST_STATISTICS = True

@pytest.fixture(scope='function')
def tracks():
    return [
            TrackFile(pkg_resources.resource_filename('pycolocstats', '../../tests/resources/test_track1.bed'),'t1'),
            TrackFile(pkg_resources.resource_filename('pycolocstats', '../../tests/resources/test_track2.bed'),'t2'),
            TrackFile(pkg_resources.resource_filename('pycolocstats', '../../tests/resources/test_track3.bed'),'t3'),
            TrackFile(pkg_resources.resource_filename('pycolocstats', '../../tests/resources/test_track4.bed'),'t4'),
            TrackFile(pkg_resources.resource_filename('pycolocstats', '../../tests/resources/test_track5.bed'), 't5'),
            TrackFile(pkg_resources.resource_filename('pycolocstats', '../../tests/resources/test_track6.bed'), 't6'),
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
    def test_default_nobg(self,chrLenFile, queryTrack, refTracks):
        selectionValues = [[('setGenomeName', u'hg19')], [('setRestrictedAnalysisUniverse', None)],
                           [('setRuntimeMode', u'quick')]]
        selectionValues.append([('setChromLenFileName', chrLenFile)])
        workingMethodObjects = WorkingMethodObjectParser(queryTrack, refTracks, selectionValues,
                                                         ALL_PYCOLOCSTATS_METHOD_CLASSES).getWorkingMethodObjects()
        selectionValues.append([('setChromLenFileName', chrLenFile)])
        methodNames = set([wmo.getMethodName() for wmo in workingMethodObjects])
        assert methodNames == set(['Giggle', 'GenometriCorr','StereoGene'])

    def test_goShifter_genome_hg38(self, tracks):
        selectionValues = [[('setGenomeName', u'hg38')],[('setRuntimeMode', u'quick')]]
        workingMethodObjects = WorkingMethodObjectParser([tracks[4]], [tracks[5]], selectionValues,
                                                         [GoShifter]).getWorkingMethodObjects()
        methodNames = set([wmo.getMethodName() for wmo in workingMethodObjects])
        assert methodNames == set(['GoShifter'])

    def test_default_inclusionbg(self,chrLenFile, queryTrack, refTracks, tracks):
        selectionValues = [[('setGenomeName', u'hg19')], [('setRestrictedAnalysisUniverse', RestrictedThroughInclusion(tracks[3]))],
                           [('setRuntimeMode', u'quick')]]
        selectionValues.append([('setChromLenFileName', chrLenFile)])
        workingMethodObjects = WorkingMethodObjectParser(queryTrack, refTracks, selectionValues,
                                                         ALL_PYCOLOCSTATS_METHOD_CLASSES).getWorkingMethodObjects()
        methodNames = set([wmo.getMethodName() for wmo in workingMethodObjects])
        assert methodNames == set(['LOLA', 'IntervalStats'])

    def test_default_inclusionbgOrNoBg(self,chrLenFile, queryTrack, refTracks, tracks):
        selectionValues = [[('setGenomeName', u'hg19')], [('setRestrictedAnalysisUniverse', RestrictedThroughInclusion(tracks[3])),('setRestrictedAnalysisUniverse', None)],
                           [('setRuntimeMode', u'quick')]]
        selectionValues.append([('setChromLenFileName', chrLenFile)])
        workingMethodObjects = WorkingMethodObjectParser(queryTrack, refTracks, selectionValues,
                                                         ALL_PYCOLOCSTATS_METHOD_CLASSES).getWorkingMethodObjects()
        methodNames = set([wmo.getMethodName() for wmo in workingMethodObjects])
        assert methodNames == set(['Giggle', 'GenometriCorr', 'IntervalStats','LOLA','StereoGene'])

    def test_adv_proximity(self,chrLenFile, queryTrack, refTracks, tracks):
        selectionValues = [[('setRestrictedAnalysisUniverse', None)], [('setColocMeasure',ColocMeasureProximity(None,None))], [('preserveClumping', False)], [('setGenomeName', u'hg19')],[('setRuntimeMode', u'quick')]]
        selectionValues.append([('setChromLenFileName', chrLenFile)])
        workingMethodObjects = WorkingMethodObjectParser(queryTrack, refTracks, selectionValues,
                                                         ALL_PYCOLOCSTATS_METHOD_CLASSES).getWorkingMethodObjects()
        methodNames = set([wmo.getMethodName() for wmo in workingMethodObjects])
        print('TEMP1: ', methodNames)
        assert methodNames == set(['IntervalStats'])


    def test_default_inclusionbgOrNoBg_stereogene(self,chrLenFile, queryTrack, refTracks, tracks):
        selectionValues = [[('setGenomeName', u'hg19')], [('setRestrictedAnalysisUniverse', RestrictedThroughInclusion(tracks[3])),('setRestrictedAnalysisUniverse', None)],
                           [('setRuntimeMode', u'quick')]]
        selectionValues.append([('setChromLenFileName', chrLenFile)])
        workingMethodObjects = WorkingMethodObjectParser(queryTrack, refTracks, selectionValues,
                                                         [StereoGene]).getWorkingMethodObjects()
        methodNames = set([wmo.getMethodName() for wmo in workingMethodObjects])
        assert methodNames == set(['StereoGene'])

