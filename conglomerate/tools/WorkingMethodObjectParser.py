from conglomerate.core.config import VERBOSE_RUNNING
from conglomerate.tools.method_compatibility import getCompatibleMethodObjects
from conglomerate.methods.genometricorr.genometricorr import GenometriCorr
from conglomerate.methods.giggle.giggle import Giggle
from conglomerate.methods.intervalstats.intervalstats import IntervalStats
from conglomerate.methods.lola.lola import LOLA
ALL_CONGLOMERATE_METHOD_CLASSES = [GenometriCorr, Giggle, IntervalStats, LOLA]

class WorkingMethodObjectParser:

    def __init__(self, queryTrack, refTracks, selectionVals, allMethodClasses):
        assert type(selectionVals)==list
        self._queryTrack = queryTrack
        self._refTracks = refTracks
        self._selectionVals = selectionVals
        self._allMethodClasses = allMethodClasses

    def getWorkingMethodObjects(self):
        if self._queryTrack is None or self._refTracks is None:
            if VERBOSE_RUNNING:
                print 'No WMOs due to lacking tracks'
            return None
        if VERBOSE_RUNNING:
            print 'Considered methods: ', ','.join([x.__name__ for x in self._allMethodClasses])
        # selectionVals = selections.values()
        workingMethodObjects = getCompatibleMethodObjects(self._selectionVals, self._queryTrack, self._refTracks,
                                                          self._allMethodClasses)
        if VERBOSE_RUNNING:
            print 'Compatible methods: ', ','.join([str(x) for x in workingMethodObjects])
        return workingMethodObjects
