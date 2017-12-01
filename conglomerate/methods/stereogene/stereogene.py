from collections import OrderedDict

from conglomerate.methods.method import OneVsOneMethod
from conglomerate.tools.constants import STEREOGENE_TOOL_NAME


class StereoGene(OneVsOneMethod):
    def __init__(self):
        self._results = None
        super(StereoGene, self).__init__()

    def _getToolName(self):
        return STEREOGENE_TOOL_NAME

    def _setDefaultParamValues(self):
        self._params['tracks'] = []

    def _setQueryTrackFileName(self, trackFn):
        self._params['tracks'] += [trackFn]

    def _setReferenceTrackFileName(self, trackFn):
        self._params['tracks'] += [trackFn]

    def setChromLenFileName(self, chromLenFileName):
        self._params['chrom'] = chromLenFileName

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is True

    def _parseResultFiles(self):
        self._results = self._parseStatisticsFile(dirpath=self._resultFilesDict['output'])

    def getPValue(self):
        return OrderedDict([(key, x['pVal']) for key, x in self._results.items()])

    def getTestStatistic(self):
        return OrderedDict([(key, x['totCorr']) for key, x in self._results.items()])

    def getFullResults(self):
        return open(self._resultFilesDict['stdout']).read()


    def preserveClumping(self, preserve):
        pass

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        pass

    def setColocMeasure(self, colocMeasure):
        pass

    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        pass

    def _parseStatisticsFile(self, dirpath):
        import xml.etree.ElementTree as et
        from os.path import join
        tree = et.parse(join(dirpath, 'statistics.xml'))
        root = tree.getroot()
        runsDict = OrderedDict()
        for run in root:
            parsedRun = self._parseRun(run)
            runsDict[(parsedRun['track1'], parsedRun['track2'])] = parsedRun
        return runsDict

    def _parseRun(self, run):
        resDict = OrderedDict()
        inputTag = run.find('input')
        resDict['track1'] = inputTag.attrib['track1']
        resDict['track2'] = inputTag.attrib['track2']
        res = run.find('res')
        resDict['totCorr'] = float(res.attrib['totCorr'])
        resDict['pVal'] = float(res.attrib['pVal'])
        return resDict

    def _printResults(self):
        print(self._results)

    def getResults(self):
        return self._results

