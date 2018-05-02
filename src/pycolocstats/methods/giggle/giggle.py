from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict

from pycolocstats.methods.interface import ColocMeasureOverlap
from pycolocstats.methods.method import OneVsManyMethod
from pycolocstats.core.types import SingleResultValue
from pycolocstats.core.constants import GIGGLE_TOOL_NAME
from pycolocstats.tools.tracks import refTrackCollRegistry

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
        self.setManualParam('genome', str(genomeName))

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

    def _setQueryTrackFileName(self, trackFile):
        bedPath = self._getBedExtendedFileName(trackFile.path)
        self._addTrackTitleMapping(bedPath, trackFile.title)
        self.qTrackFn = bedPath
        self._params['search_q'] = bedPath

    def getRefTracksMappedToIndexParams(self, trackFnList):
        if trackFnList == ['prebuilt', 'LOLACore_170206']:
            return {'trackIndex': str('LOLACore_170206'),
                    'trackCollection': str('codex'),
                   'genome': str('hg19')
                    }
        else:
            return None

    def _setReferenceTrackFileNames(self, trackFileList):
        # indexParams = self.getRefTracksMappedToIndexParams(trackFnList)
        # if indexParams != None:
        #     for key,val in indexParams.items():
        #         self.setManualParam(key, val)
        registry = refTrackCollRegistry
        if registry.isTrackCollSpec(trackFileList):
            trackIndex, trackCollection = \
                registry.getTrackIndexAndCollFromTrackCollSpec(trackFileList)
            self.setManualParam('trackIndex', str(trackIndex))
            self.setManualParam('trackCollection', str(trackCollection))
        else:
            bedPathList = []
            for trackFile in trackFileList:
                bedPath = self._getBedExtendedFileName(trackFile.path)
                import os
                self._addTrackTitleMapping(os.path.basename(bedPath)+'.gz', trackFile.title)
                bedPathList.append(bedPath)
            self._params['index_i'] = bedPathList

    def setAllowOverlaps(self, allowOverlaps):
        if allowOverlaps is False:
            self.setNotCompatible()

    def _parseResultFiles(self):
        results = GiggleResults()
        with open(self.getResultFilesDict()['stdout']) as resF:
            for line in resF:
                if line.strip().startswith('#'):
                    continue
                else:
                    vals = [self.qTrackFn] + [x.strip() for x in line.strip().split()]
                    if 'trackCollection' in self._params and vals[1].endswith('.gz'):
                        vals[1] = vals[1][:-3]
                    newResult = GiggleResult(*vals)
                    results.addResult(newResult.qFileName, newResult.fileName, newResult)
        self._parsedResults = results
        if len(results.getResults())==0:
            self.setRunSuccessStatus(False)

    def getPValue(self):
        pvalDict = self._parsedResults.getResultsPerName('pvalTwoTail')
        for key in pvalDict.keys():
            pvalDict[key] = SingleResultValue(self._getNumericFromStr(pvalDict[key]), '%.2e' % pvalDict[key])
        return self.getRemappedResultDict(pvalDict)

    @classmethod
    def getTestStatDescr(cls):
        return 'odds ratio'

    def getTestStatistic(self):
        #return self.getRemappedResultDict(self._parsedResults.getResultsPerName('overlaps'))
        testStatDict = self._parsedResults.getResultsPerName('oddsRatio')
        for key in testStatDict.keys():
            numericResult = testStatDict[key]
            textualResult = '<span title="%s">' % self.getTestStatDescr() + self._getFormattedVal(numericResult) + '</span>'
            testStatDict[key] = SingleResultValue(numericResult, textualResult)
        return self.getRemappedResultDict(testStatDict)


    def getFullResults(self):
        fullResults = self.resultsToHtml(stdoutFile=self.getResultFilesDict()['stdout'],
                                         trackTitleMapping=self._trackTitleMappings)
        return self.getRemappedResultDict(OrderedDict([(key,fullResults) for key in self._parsedResults.getResultsPerName('overlaps').keys()]))

    def preserveClumping(self, preserve):
        if preserve:
            self.setNotCompatible()

    def setRestrictedAnalysisUniverse(self, restrictedAnalysisUniverse):
        if restrictedAnalysisUniverse is not None:
            self.setNotCompatible()

    def setColocMeasure(self, colocMeasure):
        if not isinstance(colocMeasure,ColocMeasureOverlap) or colocMeasure._countWholeIntervals is False:
            self.setNotCompatible()


    def setHeterogeneityPreservation(self, preservationScheme, fn=None):
        if preservationScheme != self.PRESERVE_HETEROGENEITY_NOT:
            self.setNotCompatible()

    def getErrorDetails(self):
        assert not self.ranSuccessfully()
        #Not checked if informative
        if self._resultFilesDict is not None and 'stderr' in self._resultFilesDict:
            return open(self._resultFilesDict['stderr']).read()
        else:
            return 'Giggle produced no error output!'

    ##############################Code by tool author:####################################

    @classmethod
    def html_headers(cls):
        return '<!DOCTYPE html> <html> <body>'

    @classmethod
    def html_footers(cls):
        return '</body></html>'

    @classmethod
    def get_rgba_str(cls, v, V, v_mid):
        min_v = min(V)
        max_v = max(V)
        from matplotlib import colors as mcolors

        _seismic_data = ((0.0, 0.0, 0.3),
                         (0.0, 0.0, 1.0),

                         (1.0, 1.0, 1.0),

                         (1.0, 0.0, 0.0),
                         (0.5, 0.0, 0.0))

        hm = mcolors.LinearSegmentedColormap.from_list( \
            name='red_white_blue', \
            colors=_seismic_data, N=256)

        mapped_v = v_mid

        if v_mid == None:
            mapped_v = (float(v) - float(min_v)) / (float(max_v) - float(min_v))
        else:
            if v > v_mid:
                mapped_v = (float(v) / float(max_v)) / 2.0 + 0.5
            elif v < v_mid:
                mapped_v = 0.5 - (float(v) / float(min_v)) / 2.0

        floats = hm(mapped_v)
        ints = [int(255 * x) for x in floats[:-1]]
        ints.append(0.5)

        rgba = 'rgba(' + ','.join([str(x) for x in ints]) + ')'

        return rgba

    @classmethod
    def html_empty_stdout(cls, stderrFile=None, printStdErr=False):
        htmlStr = '''
               <p>Giggle produced no results<p>
           '''
        from os import linesep
        if stderrFile and printStdErr:
            with open(stderrFile, "rt") as f:
                htmlStr += "<p>Error:<br>"
                htmlStr += f.read().replace(linesep, "<br>")
                htmlStr += "</p>"

        return htmlStr

    @classmethod
    def resultsToHtml(cls, outputFolder=None, stdoutFile=None, stderrFile=None, trackTitleMapping=None):
        from os.path import sep
        if not stdoutFile:
            return cls.html_headers() + cls.html_empty_stdout(stderrFile, True) + cls.html_footers()

        html_string = cls.html_headers()

        html_string += '<table style="text-align: left;" >'
        header = None
        rows = []

        giggle_scores = []
        odds_ratios = []
        fisher_two_tails = []

        for l in open(stdoutFile, 'rt'):
            if header == None:
                header = l[1:].rstrip().split()
            else:
                A = l.rstrip().split()
                rows.append(A)
                giggle_scores.append(float(A[7]))
                odds_ratios.append(float(A[3]))
                fisher_two_tails.append(float(A[4]))

        html_string += '<tr>'
        html_string += ' '.join(['<th>' + x.replace('_', ' ') + '</th>' for x in header])
        html_string += '</tr>'

        rows.sort(key=lambda x: float(x[7]), reverse=True)

        for row in rows:

            html_string += '<tr>'
            i = 0
            for x in row:
                if i == 0:
                    trackTitle = trackTitleMapping[x.split(sep)[-1]]
                    html_string += '<td>' + trackTitle + '</td>'
                elif i == 3:
                    odds_ratio = float(x)
                    rgba = cls.get_rgba_str(odds_ratio, odds_ratios, 1.0)
                    html_string += '<td  style="background-color: ' + rgba + ';">' + x + '</td>'
                elif i == 4:
                    fisher_two_tail = float(x)
                    rgba = cls.get_rgba_str(fisher_two_tail, fisher_two_tails, None)
                    html_string += '<td  style="background-color: ' + rgba + ';">' + x + '</td>'
                elif i == 7:
                    giggle_score = float(x)
                    rgba = cls.get_rgba_str(giggle_score, giggle_scores, 0.0)
                    html_string += '<td  style="background-color: ' + rgba + ';">' + x + '</td>'
                else:
                    html_string += '<td>' + x + '</td>'
                i += 1
            html_string += '</tr>\n'

        html_string += '</table>'

        html_string += cls.html_footers()

        return html_string


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
        return list(self.getResultsPerName(resName=resName).values())

    def __repr__(self):
        firstLine = "#file	file_size	overlaps	odds_ratio	fishers_two_tail	fishers_left_tail	fishers_rigth_tail	combo_score"
        return "\n".join([firstLine] + [str(val) for val in self.getResults().values()])

