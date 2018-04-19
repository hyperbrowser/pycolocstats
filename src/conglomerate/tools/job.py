from __future__ import absolute_import, division, print_function, unicode_literals
from future.standard_library import install_aliases

import cwltool
import logging
import os

from conglomerate.core.config import VERBOSE_RUNNING, DEFAULT_JOB_OUTPUT_DIR
from conglomerate.core.types import PathStr, PathStrList
from conglomerate.tools.cache import ToolResultsCacher

install_aliases()
from urllib.parse import urlparse

__metaclass__ = type


class Job(object):
    def __init__(self, tool, params, jobOutputDir=DEFAULT_JOB_OUTPUT_DIR):
        self._tool = tool
        self._params = params
        self._jobOutputDir = jobOutputDir

    def run(self):
        try:
            if not VERBOSE_RUNNING:
                logging.getLogger("cwltool").disabled = 1
            params = self._mapParamsToCwl(self._params)
            #added caching:
            cacher = ToolResultsCacher(self._tool, self._params)
            if cacher.cacheAvailable():
                toolResults = cacher.load()
            else:
                cwlTool = self._tool.getCwlTool(self._jobOutputDir)
                toolResults = cwlTool(**params)
                cacher.store(toolResults)
            return self._createResultFilesDict(toolResults)
        except cwltool.factory.WorkflowStatus as ws:
            return self._createResultFilesDict(ws.out)

    @staticmethod
    def _createResultFilesDict(toolResults):
        resultFilesDict = {}
        assert isinstance(toolResults, dict)
        for key, fileinfo in toolResults.items():
            assert isinstance(fileinfo, dict)
            parsedLocation = urlparse(fileinfo['location'])
            assert parsedLocation.scheme == 'file'
            resultFilesDict[key] = parsedLocation.path
        return resultFilesDict

    @staticmethod
    def _mapParamsToCwl(params):
        retParams = {}
        for key, val in params.items():
            if isinstance(val, PathStr):
                retParams[key] = {'class': 'File', 'location': val}
            elif isinstance(val, PathStrList):
                retParams[key] = [{'class': 'File', 'location': f} for f in val]
            else:
                retParams[key] = val
        return retParams
