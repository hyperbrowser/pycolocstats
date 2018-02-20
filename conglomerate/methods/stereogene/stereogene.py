from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

from conglomerate.methods.method import OneVsOneMethod
from conglomerate.core.types import SingleResultValue
from conglomerate.core.constants import STEREOGENE_TOOL_NAME
import os

__metaclass__ = type


class StereoGene(OneVsOneMethod):
    def __init__(self):
        self._results = None

        #TODO: Remove this temporary fix when tool author has resolved why query and ref titles are sometimes mixed..
        self._queryTitle = None
        self._refTitle = None

        super(StereoGene, self).__init__()

    def _getToolName(self):
        return STEREOGENE_TOOL_NAME

    def _setDefaultParamValues(self):
        self._params['tracks'] = []

    def setGenomeName(self, genomeName):
        pass

    def setChromLenFileName(self, chromLenFileName):
        self._params['chrom'] = chromLenFileName

    def _setQueryTrackFileName(self, trackFile):
        bedPath = self._getBedExtendedFileName(trackFile.path)
        self._addTrackTitleMapping(os.path.basename(bedPath), trackFile.title)
        self._params['tracks'] += [bedPath]
        self._queryTitle = trackFile.title


    def _setReferenceTrackFileName(self, trackFile):
        if trackFile is not in ['prebuilt', 'LOLACore_170206']:
            self.setNotCompatible()
        #assert trackFile not in ['prebuilt', 'LOLACore_170206']
        bedPath = self._getBedExtendedFileName(trackFile.path)
        self._addTrackTitleMapping(os.path.basename(bedPath), trackFile.title)
        self._params['tracks'] += [bedPath]
        self._refTitle = trackFile.title

    def setAllowOverlaps(self, allowOverlaps):
        if allowOverlaps is not False:
            self.setNotCompatible()
        #assert allowOverlaps is True

    def _parseResultFiles(self):
        self._results = self._parseStatisticsFile(dirpath=self._resultFilesDict['output'])

    def getPValue(self):
        return self.getRemappedResultDict(OrderedDict([
            (key, SingleResultValue(x['pVal'],
                                    str(x['pVal']))) for key, x in self._results.items()]))

    def getTestStatistic(self):
        return self.getRemappedResultDict(
            OrderedDict([(key,
                          SingleResultValue(x['Fg_Corr'],
                                            '<span title="' + \
                                            self.getTestStatDescr() \
                                            + '">'+'%.5f'%x['Fg_Corr']+'</span>'))
            for key, x in self._results.items()]))

    @classmethod
    def getTestStatDescr(cls):
        return 'Correlation coefficient'

    def getFullResults(self):
        fullResults = open(self._resultFilesDict['stdout']).read().replace('\n','<br>\n')
        return self.getRemappedResultDict(OrderedDict([(key, fullResults) for key in self._results.keys()]))

    def preserveClumping(self, preserve):
        if preserve == True:
            self.setNotCompatible()
        #assert preserve is False, preserve

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        if restrictedAnalysisUniverse is not None:
            self.setNotCompatible()
        #assert restrictedAnalysisUniverse is None, restrictedAnalysisUniverse

    def setColocMeasure(self, colocMeasure):
        from conglomerate.methods.interface import ColocMeasureCorrelation
        if not isinstance(colocMeasure, ColocMeasureCorrelation) and not type(colocMeasure):
            self.setNotCompatible()
        #assert isinstance(colocMeasure, ColocMeasureCorrelation), type(colocMeasure)

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        if preservationScheme is not None:
            self.setNotCompatible()
        #assert preservationScheme is None, preservationScheme

    def _parseStatisticsFile(self, dirpath):
        import xml.etree.ElementTree as et
        from os.path import join
        tree = et.parse(join(dirpath, 'statistics.xml'))
        root = tree.getroot()
        runsDict = OrderedDict()
        for run in root:
            parsedRun = self._parseRun(run)
            if parsedRun['track1']==self._refTitle and parsedRun['track2']==self._queryTitle:
                runsDict[(parsedRun['track2'], parsedRun['track1'])] = parsedRun
            else:
                #The original code
                runsDict[(parsedRun['track1'], parsedRun['track2'])] = parsedRun
        return runsDict

    def _parseRun(self, run):
        resDict = OrderedDict()
        inputTag = run.find('input')
        resDict['track1'] = inputTag.attrib['track1']
        resDict['track2'] = inputTag.attrib['track2']
        res = run.find('res')
        resDict['Fg_Corr'] = float(res.attrib['Fg_Corr'])
        resDict['pVal'] = float(res.attrib['pVal'])
        return resDict

    def _printResults(self):
        print(self._results)

    def getResults(self):
        return self._results

    def getErrorDetails(self):
        assert not self.ranSuccessfully()
        #Not checked if informative
        if self._resultFilesDict is not None and 'stderr' in self._resultFilesDict:
            return open(self._resultFilesDict['stderr']).read().replace('\n','<br>\n')
        else:
            return 'Stereogene did not provide any error output'

    def setRuntimeMode(self, mode):
        #also set corrOnly!?
        if mode =='quick':
            numPerm = 100
        elif mode == 'medium':
            numPerm = 1000
        elif mode == 'accurate':
            numPerm = 10000
        else:
            raise Exception('Invalid mode')
        self.setManualParam('nShuffle', numPerm)


# The StereoGene program compares pairs of tracks and calculates kernel correlations
# Usage:
# $ ./StereoGene [-parameters] trackFile_1 trackFile_2 ... trackFile_n
#
#
# ====================== common parameters ======================
# -v 	verbose
# -syntax 	strong syntax control in input files
# -verbose <0|1>	verbose
# -s 	no output to stdout
# -silent <0|1>	no output to stdout
#
# ====================== preparation parameters ======================
# -bin <int>	bin size for input averaging
# -clear <0|1>	force binary profile preparation
# -c 	force  binary profile preparation
#
# ====================== paths and files ======================
# -cfg <string>	config file
# -profPath <string>	path for binary profiles
# -trackPath <string>	path for tracks
# -resPath <string>	path for results
# -confounder <string>	confounder filename
# -statistics <string>	cumulative file with statistics
# -params <string>	cumulative file with parameters
# -log <string>	cumulative log-file
#
# ====================== input parameters ======================
# -chrom <string>	chromosome file
# -BufSize <int>	Buffer Size
# -bpType <SCORE|SIGNAL|LOGPVAL> 	The value used as a score for BroadPeak input file
# -pcorProfile <string>	Track for partial correlation
# -NA 	use NA values as unknown and fill them by noise
# -threshold <int>	threshold for input data for removing too small values: 0..250
#
# ====================== Analysis parameters ======================
# -kernelSigma <float>	Kernel width
# -wSize <int>	Window size
# -maxNA <float>	Max number of NA values in window (percent)
# -maxZero <float>	Max number of zero values in window (percent)
# -nShuffle <int>	Number of shuffles for background calculation
#
# ====================== Output parameters ======================
# -outSpectr <0|1>	write fourier spectrums
# -outChrom <0|1>	write statistics by chromosomes
# -writeDistr <0|1>	write foreground and background distributions
# -r 	write R script for the result presentation
# -crossWidth 	Width of cross-correlation plot
# -Distances 	Write distance correlations
# -outLC <0|1>	parameters for local correlation file
# -lc 	produce profile correlation
# -LCScale <LOG|LIN> 	Local correlation scale: LOG | LIN
# -L_FDR <float>	threshold on left FDR when write the local correlation
# -R_FDR <float>	threshold on right FDR when write the local correlation
# -outRes <NONE|XML|TAB|BOTH> 	format for results in statistics file
