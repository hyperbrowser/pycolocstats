from itertools import product
from tempfile import NamedTemporaryFile

import os
import pkg_resources
import pytest

from conglomerate.methods.genometricorr.genometricorr import GenometriCorr
from conglomerate.methods.giggle.giggle import Giggle
from conglomerate.methods.goshifter.goshifter import GoShifter
from conglomerate.methods.interface import RestrictedThroughInclusion
from conglomerate.methods.intervalstats.intervalstats import IntervalStats
from conglomerate.methods.lola.lola import LOLA
from conglomerate.methods.multimethod import MultiMethod
from conglomerate.methods.stereogene.stereogene import StereoGene
from conglomerate.tools.TrackFile import TrackFile
from conglomerate.tools.runner import runAllMethodsInSequence


@pytest.fixture(scope='function')
def tracks():
    pass

@pytest.fixture(scope='function')
def chrLenFile():
    return pkg_resources.resource_filename('tests.resources', 'chrom_lengths.tabular')


@pytest.mark.usefixtures('chrLenFile', 'tracks')
class TestMethods(object):
    def test_giggle_oneVsManyDatFiles_noOverlap(self):
        raise Exception('Boris should add')
        selections = {} #BIG
        giggle = getTestableMethod(Giggle, selections, [tracks[0]])
        commandUsed = ''
        print 'Command used: ', commandUsed
        runAllMethodsInSequence((giggle))
        assert giggle.something == somethingElse

    def test_goShifter_oneVsManyDatFiles_noOverlap(self):
        raise Exception('Diana is awaiting Trynka')

    def test_intervalStats_oneVsManyDatFiles_noOverlap(self):
        raise Exception('Diana should add')