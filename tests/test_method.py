from tempfile import NamedTemporaryFile

from conglomerate.methods.genometricorr.genometricorr import GenometriCorr
from conglomerate.tools.runner import runAllMethodsInSequence


class TestMethods(object):
    def testGenometriCorr(self):
        track1, track2, chrlist, chrlen = self._getSampleFileNames()
        method = GenometriCorr()
        method.setTrackFileNames([track1.name, track2.name])
        method.setChromLenFileName(chrlen.name)
        method.setManualParam('chrlist', chrlist.name)
        method.setManualParam('t1Format', 'bed')
        method.setManualParam('t2Format', 'bed')
        method.setManualParam('ecdfPermNum', 5)
        method.setManualParam('meanPermNum', 5)
        method.setManualParam('jaccardPermNum', 5)
        runAllMethodsInSequence([method])
        self._printResultFiles(method, ['stderr', 'stdout'])

    @staticmethod
    def _getSampleFileNames():
        track1 = TestMethods._getSampleFileName('chr1\t213941196\t213942363\n'
                                                'chr1\t213942363\t213943530\n'
                                                'chr1\t213943537\t213944697\n'
                                                'chr2\t158364697\t158365864\n'
                                                'chr2\t158365864\t158367031\n'
                                                'chr3\t127477031\t127478198\n'
                                                'chr3\t127478198\t127479365\n'
                                                'chr3\t127479365\t127480532\n'
                                                'chr3\t127480532\t127481699\n')
        track2 = TestMethods._getSampleFileName('chr1\t213941196\t213942363\n'
                                                'chr1\t213942363\t213943530\n'
                                                'chr1\t213943530\t213944697\n'
                                                'chr2\t158364697\t158365864\n'
                                                'chr2\t158365864\t158367031\n'
                                                'chr3\t127477031\t127478198\n'
                                                'chr3\t127478198\t127479365\n'
                                                'chr3\t127479365\t127480532\n'
                                                'chr3\t127480532\t127481699\n')
        chrlist = TestMethods._getSampleFileName('chr1\n'
                                                 'chr2\n'
                                                 'chr3\n')
        chrlen = TestMethods._getSampleFileName('chr1=249250621\n'
                                                'chr2=249250621\n'
                                                'chr3=249250621\n')
        return track1, track2, chrlist, chrlen

    @staticmethod
    def _getSampleFileName(contents):
        sampleFile = NamedTemporaryFile(mode='w+', dir='/tmp')
        sampleFile.write(contents)
        sampleFile.flush()
        return sampleFile

    @staticmethod
    def _printResultFiles(method, keys):
        for key in keys:
            print(key, '\n------\n', open(method.getResultFilesDict()[key]).read())
