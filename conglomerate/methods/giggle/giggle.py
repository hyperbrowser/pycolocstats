from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

from conglomerate.methods.interface import ColocMeasureOverlap
from conglomerate.methods.method import OneVsManyMethod
from conglomerate.tools.constants import GIGGLE_TOOL_NAME

__metaclass__ = type

class Giggle(OneVsManyMethod):
    def __init__(self):
        self.qTrackFn = None
        self._parsedResults = None
        super(Giggle, self).__init__()

    def _getToolName(self):
        return GIGGLE_TOOL_NAME

    def _setDefaultParamValues(self):
        self.setManualParam('search_s', True)
        self.setManualParam('index_o', str('index'))
        self.setManualParam('search_i', str('index'))

    def setGenomeName(self, genomeName):
        assert genomeName == 'hg19'

    def setChromLenFileName(self, chromLenFileName):
        genomeLength = 0
        with open(chromLenFileName) as f:
            for line in f:
                if not line.strip().startswith('#'):
                    vals = line.strip().split()
                    assert len(vals) == 2, "Invalid chromlen file line %s" % line
                    try:
                        genomeLength += int(vals[1].strip())
                    except:
                        raise ValueError(line)
        if genomeLength:
            self.setManualParam('search_g', genomeLength)

    def _setQueryTrackFileName(self, trackFn):
        self.qTrackFn = trackFn
        self._params['search_q'] = trackFn

    def _setReferenceTrackFileNames(self, trackFnList):
        self._params['index_i'] = trackFnList

    def setAllowOverlaps(self, allowOverlaps):
        assert allowOverlaps is True

    def _parseResultFiles(self):
        results = GiggleResults()
        with open(self.getResultFilesDict()['stdout']) as resF:
            for line in resF:
                if line.strip().startswith('#'):
                    continue
                else:
                    vals = [self.qTrackFn] + [x.strip() for x in line.strip().split()]
                    newResult = GiggleResult(*vals)
                    results.addResult(newResult.qFileName, newResult.fileName, newResult)
        self._parsedResults = results

    def getPValue(self):
        return self._parsedResults.getResultsPerName('pvalTwoTail')

    def getTestStatistic(self):
        return self._parsedResults.getResultsPerName('overlaps')

    def getFullResults(self):
        return open(self.getResultFilesDict()['stdout']).read()

    def preserveClumping(self, preserve):
        assert preserve is False

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        assert restrictedAnalysisUniverse is False

    def setColocMeasure(self, colocMeasure):
        assert isinstance(colocMeasure,ColocMeasureOverlap)
        assert colocMeasure._countWholeIntervals is True


    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        assert preservationScheme is False


class GiggleResult(object):
    def __init__(self, qFilePath, filePath, fileSize, overlaps, oddsRatio, pvalTwoTail, pvalLeftTail, pvalRightTail, comboScore):
        self.qFileName = self._getFileNameFromPath(qFilePath)
        self.qFilePath = qFilePath
        self.fileName = self._getFileNameFromPath(filePath)
        self.filePath = filePath
        self.fileSize = float(fileSize)
        self.overlaps = float(overlaps)
        self.oddsRatio = float(oddsRatio)
        self.pvalTwoTail = float(pvalTwoTail)
        self.pvalLeftTail = float(pvalLeftTail)
        self.pvalRightTail = float(pvalRightTail)
        self.comboScore = float(comboScore)

    def _getFileNameFromPath(self, filePath):
        import ntpath
        head, tail = ntpath.split(filePath)
        return tail or ntpath.basename(head)

    def __repr__(self):
        return "\t".join([str(x) for x in [self.filePath,
                                           self.fileSize,
                                           self.overlaps,
                                           self.oddsRatio,
                                           self.pvalTwoTail,
                                           self.pvalLeftTail,
                                           self.pvalRightTail,
                                           self.comboScore]])


class GiggleResults(object):
    def __init__(self):
        self._results = OrderedDict()

    def getResults(self):
        return self._results

    def addResult(self, track1, track2, result):
        assert isinstance(result, GiggleResult), type(result)
        self._results[(track1, track2)] = result

    def getResultsPerName(self, resName):
        assert resName in ['filePath', 'fileSize', 'overlaps', 'oddsRatio', 'pvalTwoTail', 'pvalLeftTail', 'pvalRightTail', 'comboScore']
        results = OrderedDict()
        for key, val in self._results.items():
            if hasattr(val, resName):
                results[key] = getattr(val, resName)
        return results

    def getResultsPerNameList(self, resName):
        return self.getResultsPerName(resName=resName).values()

    def __repr__(self):
        firstLine = "#file	file_size	overlaps	odds_ratio	fishers_two_tail	fishers_left_tail	fishers_rigth_tail	combo_score"
        return "\n".join([firstLine] + [str(val) for val in self.getResults().values()])

