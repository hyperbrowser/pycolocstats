from pycolocstats.core.config import VERBOSE_RUNNING
from pycolocstats.methods.goshifter.goshifter import GoShifter
from pycolocstats.methods.stereogene.stereogene import StereoGene
from pycolocstats.tools.method_compatibility import getCompatibleMethodObjects
from pycolocstats.methods.genometricorr.genometricorr import GenometriCorr
from pycolocstats.methods.giggle.giggle import Giggle
from pycolocstats.methods.intervalstats.intervalstats import IntervalStats
from pycolocstats.methods.lola.lola import LOLA
ALL_PYCOLOCSTATS_METHOD_CLASSES = [GenometriCorr, Giggle, IntervalStats, LOLA, StereoGene, GoShifter]

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
                print('No WMOs due to lacking tracks')
            return None
        if VERBOSE_RUNNING:
            print('Considered methods: ', ','.join([x.__name__ for x in self._allMethodClasses]))
        # selectionVals = selections.values()
        workingMethodObjects = getCompatibleMethodObjects(self._selectionVals, self._queryTrack, self._refTracks,
                                                          self._allMethodClasses)
        if VERBOSE_RUNNING:
            print('Compatible methods: ', ','.join([str(x) for x in workingMethodObjects]))
        return workingMethodObjects
