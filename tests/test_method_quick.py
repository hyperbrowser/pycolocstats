import os
import pkg_resources
import pytest

from conglomerate.core.types import TrackFile
from conglomerate.methods.genometricorr.genometricorr import GenometriCorr
from conglomerate.methods.multimethod import MultiMethod
from conglomerate.methods.stereogene.stereogene import StereoGene
from conglomerate.tools.runner import runAllMethodsInSequence


@pytest.fixture(scope='function')
def tracks():
    return [
            TrackFile(pkg_resources.resource_filename('tests', 'resources/test_track1.bed'),''),
            TrackFile(pkg_resources.resource_filename('tests', 'resources/test_track2.bed'),''),
            TrackFile(pkg_resources.resource_filename('tests', 'resources/test_track3.bed'),''),
            TrackFile(pkg_resources.resource_filename('tests', 'resources/test_track4.bed'),''),
            ]


@pytest.fixture(scope='function')
def chrLenFile():
    return pkg_resources.resource_filename('tests', 'resources/test_chrom_lengths_2.tabular')


@pytest.mark.usefixtures('chrLenFile', 'tracks')
class TestMethods(object):

    def testStereoGene(self, chrLenFile, tracks):
        method = StereoGene()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('v', True)
        method.setManualParam('silent', 0)
        method.setManualParam('wSize', 20)
        method.setManualParam('bin', 5)
        method.setManualParam('kernelSigma', 10.0)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        self._assertMethodResultsSize(1, method)

    def testGenometriCorr(self, chrLenFile, tracks):
        # raise Exception('With current setup, too long running time to function as unit test')
        method = GenometriCorr()
        method.setQueryTrackFileNames([tracks[0]])
        method.setReferenceTrackFileNames([tracks[1]])
        method.setChromLenFileName(chrLenFile)
        method.setManualParam('ecdfPermNum', 5)
        method.setManualParam('meanPermNum', 5)
        method.setManualParam('jaccardPermNum', 5)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout', 'output'])
        print(method.getPValue())
        print(method.getTestStatistic())

    @staticmethod
    def _assertMethodResultsSize(expectedResulstNr, method):
        assert expectedResulstNr == len(method.getTestStatistic()), \
            "%s: Expected %i test statistic results got %i (got teststat: %s)" % (
                str(method), expectedResulstNr, len(method.getTestStatistic()), method.getTestStatistic())
        assert expectedResulstNr == len(method.getPValue()), \
            "%s: Expected %i p-values got %i" % (str(method), expectedResulstNr, len(method.getPValue()))

    @staticmethod
    def _printResultFiles(method, keys):
        if isinstance(method, MultiMethod):
            resultFilesDictList = method.getResultFilesDictList()
        else:
            resultFilesDictList = [method.getResultFilesDict()]

        for resultFilesDict in resultFilesDictList:
            for key in keys:
                assert key in resultFilesDict, (key,resultFilesDict)
                print(key)
                print('------')
                print('Local path: ' + resultFilesDict[key])
                print('------')
                print('\n'.join(os.listdir(resultFilesDict[key])) if key == 'output'
                else open(resultFilesDict[key]).read())