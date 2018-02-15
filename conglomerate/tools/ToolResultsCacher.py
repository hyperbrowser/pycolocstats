from conglomerate.core.config import VERBOSE_RUNNING

STORE_IN_CACHE = False
LOAD_FROM_CACHE = False
import pickle
import os


class ToolResultsCacher(object):
    #CACHE_DISK_PATH = '/Users/sandve/egne_dokumenter/_faglig/conglomerateColoc/cache/'
    CACHE_DISK_PATH = '/data/tmp/congloTmp/toolResultsCache/'
    def __init__(self, tool, params):
        self._toolName = tool._toolName
        self._params = params
        cache_params = {}
        for key,val in self._params.items():
            if isinstance(val,list):
                val = tuple(val)
            cache_params[key] = val
        try:
            self._cacheKey = str(hash((self._toolName, tuple(sorted(cache_params.items())))))
            self._cacheFn = self.CACHE_DISK_PATH + self._cacheKey + '_results.pickle'
            self._cacheContentsFn = self.CACHE_DISK_PATH + self._cacheKey + '_fileContents.pickle'

        except:
            self._cacheKey = None
            self._cacheFn = None
            if VERBOSE_RUNNING:
                print('Not able to determine cache key for method: ', self._toolName, 'based on params: ', repr(self._params))
                import traceback
                traceback.print_exc()
            #self._cacheKey = str(hash((self._toolName, tuple(sorted([x for x in self._params.items() if not x[1].startswith('/tmp')] )))))
        #print('TEMP2: ', tuple(sorted(self._params.items())))

    def store(self, toolResults):
        if STORE_IN_CACHE and self._cacheFn is not None:
            pickle.dump(toolResults, open(self._cacheFn,'w'))
            #At least for now, also needs to cache file contents
            # fileContents = {}
            # for key, fileinfo in toolResults.items():
            #     if not
            #     from urlparse import urlparse
            #     parsedLocation = urlparse(fileinfo['location'])
            #     fileContents[parsedLocation.path] = open(parsedLocation.path).read()
            # pickle.dump(fileContents, open(self._cacheContentsFn,'w'))



    def load(self):
        if self.cacheAvailable():
            if VERBOSE_RUNNING:
                print('Loading cached results for: ', self._toolName)
            toolResults = pickle.load(open(self._cacheFn))
            for key, fileinfo in toolResults.items():
                from urlparse import urlparse
                parsedLocation = urlparse(fileinfo['location'])
                import os
                if not os.path.exists(parsedLocation.path):
                    return None

            #reconstruct file contents:
            # fileContents = pickle.load(open(self._cacheContentsFn))
            # for key, fileinfo in toolResults.items():
            #     from urlparse import urlparse
            #     parsedLocation = urlparse(fileinfo['location'])
            #     open(parsedLocation.path, 'w').write(fileContents[parsedLocation.path])

            return toolResults
        else:
            return None

    def cacheAvailable(self):
        if LOAD_FROM_CACHE and self._cacheFn is not None:
            if VERBOSE_RUNNING and not os.path.exists(self._cacheFn):
                print('No cached result found: ', {'Tool: ':self._toolName, 'Params: ':self._params.items()})
            return os.path.exists(self._cacheFn)
        else:
            return False
