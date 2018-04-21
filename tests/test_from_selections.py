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
from pycolocstats.tools.WorkingMethodObjectParser import ALL_PYCOLOCSTATS_METHOD_CLASSES
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

        '''Lola stderr output:
        Loading required package: BiocGenerics
        Loading required package: parallel
        
        Attaching package: 'BiocGenerics'
        
        The following objects are masked from 'package:parallel':
        
            clusterApply, clusterApplyLB, clusterCall, clusterEvalQ,
            clusterExport, clusterMap, parApply, parCapply, parLapply,
            parLapplyLB, parRapply, parSapply, parSapplyLB
        
        The following objects are masked from 'package:stats':
        
            IQR, mad, xtabs
        
        The following objects are masked from 'package:base':
        
            Filter, Find, Map, Position, Reduce, anyDuplicated, append,
            as.data.frame, as.vector, cbind, colnames, do.call, duplicated,
            eval, evalq, get, grep, grepl, intersect, is.unsorted, lapply,
            lengths, mapply, match, mget, order, paste, pmax, pmax.int, pmin,
            pmin.int, rank, rbind, rownames, sapply, setdiff, sort, table,
            tapply, union, unique, unlist, unsplit
        
        Loading required package: S4Vectors
        Loading required package: stats4
        Loading required package: IRanges
        Loading required package: GenomeInfoDb
        Reading collection annotations: 
            In collection 'collection', consider adding a 'collection.txt' annotation file.
        Reading region annotations...
        ::Creating cache::	regiondb/collection//collection_files.RData
        regiondb//collection/regions
            In 'collection', no index file. Found 1 files
        to load with defaults (filename only)
        Collection: collection. Creating size file...
        collection
        ::Creating cache::	regiondb/collection/collection.RData
        Reading 1 files...
        1: regiondb/collection/regions/test_track2.bed
        Warning messages:
        1: In `[.data.table`(indexDT, , `:=`(col, as.character(NA)), with = FALSE) :
          with=FALSE together with := was deprecated in v1.9.4 released Oct 2014. Please wrap the LHS of := with parentheses; e.g., DT[,(myVar):=sum(b),by=a] to assign to column name(s) held in variable myVar. See ?':=' for other examples. As warned in 2014, this is now a warning.
        2: In `[.data.table`(indexDT, , `:=`(col, as.character(NA)), with = FALSE) :
          with=FALSE together with := was deprecated in v1.9.4 released Oct 2014. Please wrap the LHS of := with parentheses; e.g., DT[,(myVar):=sum(b),by=a] to assign to column name(s) held in variable myVar. See ?':=' for other examples. As warned in 2014, this is now a warning.
        3: In `[.data.table`(indexDT, , `:=`(col, as.character(NA)), with = FALSE) :
          with=FALSE together with := was deprecated in v1.9.4 released Oct 2014. Please wrap the LHS of := with parentheses; e.g., DT[,(myVar):=sum(b),by=a] to assign to column name(s) held in variable myVar. See ?':=' for other examples. As warned in 2014, this is now a warning.
        4: In `[.data.table`(indexDT, , `:=`(col, as.character(NA)), with = FALSE) :
          with=FALSE together with := was deprecated in v1.9.4 released Oct 2014. Please wrap the LHS of := with parentheses; e.g., DT[,(myVar):=sum(b),by=a] to assign to column name(s) held in variable myVar. See ?':=' for other examples. As warned in 2014, this is now a warning.
        5: In `[.data.table`(indexDT, , `:=`(col, as.character(NA)), with = FALSE) :
          with=FALSE together with := was deprecated in v1.9.4 released Oct 2014. Please wrap the LHS of := with parentheses; e.g., DT[,(myVar):=sum(b),by=a] to assign to column name(s) held in variable myVar. See ?':=' for other examples. As warned in 2014, this is now a warning.
        6: In `[.data.table`(indexDT, , `:=`(col, as.character(NA)), with = FALSE) :
          with=FALSE together with := was deprecated in v1.9.4 released Oct 2014. Please wrap the LHS of := with parentheses; e.g., DT[,(myVar):=sum(b),by=a] to assign to column name(s) held in variable myVar. See ?':=' for other examples. As warned in 2014, this is now a warning.
        Converting GRanges to GRangesList.
        Calculating unit set overlaps...
        Calculating universe set overlaps...
        Calculating Fisher scores...
        Warning message:
        In runLOLA(userset, useruniverse, regionDB, minOverlap = 1, cores = 1,  :
          Negative b entry in table. This means either: 1) Your user sets contain items outside your universe; or 2) your universe has a region that overlaps multiple user set regions, interfering with the universe set overlap calculation.
        Error in unique(collection) : 
          error in evaluating the argument 'x' in selecting a method for function 'unique': Error: object 'collection' not found
        Calls: writeCombinedEnrichment -> [ -> [.data.table -> eval -> eval -> unique
        Execution halted
        '''

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

