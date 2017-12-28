from conglomerate.tools.constants import VERBOSE_RUNNING

STORE_IN_CACHE = True
LOAD_FROM_CACHE = True
import pickle
import os


class ToolResultsCacher(object):
    #CACHE_DISK_PATH = '/Users/sandve/egne_dokumenter/_faglig/conglomerateColoc/cache/'
    CACHE_DISK_PATH = '/data/tmp/congloTmp/'
    def __init__(self, tool, params):
        self._toolName = tool._toolName
        self._params = params
        try:
            self._cacheKey = str(hash((self._toolName, tuple(sorted(self._params.items())))))
            self._cacheFn = self.CACHE_DISK_PATH + self._cacheKey
        except:
            self._cacheKey = None
            self._cacheFn = None
            #self._cacheKey = str(hash((self._toolName, tuple(sorted([x for x in self._params.items() if not x[1].startswith('/tmp')] )))))
        #print('TEMP2: ', tuple(sorted(self._params.items())))

    def store(self, toolResults):
        if STORE_IN_CACHE:
            pickle.dump(toolResults, open(self._cacheFn,'w'))

    def load(self):
        if self.cacheAvailable():
            if VERBOSE_RUNNING:
                print 'Loading cached results for: ', self._toolName
            return pickle.load(open(self._cacheFn))
        else:
            return None

    def cacheAvailable(self):
        if LOAD_FROM_CACHE and self._cacheFn is not None:
            return os.path.exists(self._cacheFn)
        else:
            return False