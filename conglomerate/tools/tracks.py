import os
from collections import defaultdict

from conglomerate.core.config import REF_COLL_GSUITES_PATH


class RefTrackCollectionRegistry(object):
    PREBUILT = '__prebuilt__'

    def __init__(self):
        self._genome2TrackIndexReg = defaultdict(set)
        self._trackIndex2CollectionReg = defaultdict(set)
        self._allCollections = set()

        if not os.path.exists(REF_COLL_GSUITES_PATH):
            return

        for root, dirs, files in os.walk(REF_COLL_GSUITES_PATH):
            for fn in files:
                trackIndex, genome, trackCollection = os.path.join(root, fn).split(os.sep)[-3:]
                self._genome2TrackIndexReg[genome].add(trackIndex)
                if not trackCollection.endswith('.gsuite'):
                    continue
                trackCollection = trackCollection[:-7]
                self._trackIndex2CollectionReg[trackIndex].add(trackCollection)
                self._allCollections.add(trackCollection)

    def getTrackCollectionList(self, genome):
        if genome not in self._genome2TrackIndexReg:
            return []

        collStrList = []
        for trackIndex in sorted(self._genome2TrackIndexReg[genome]):
            for trackCollection in sorted(self._trackIndex2CollectionReg[trackIndex]):
                collStrList.append('{}: {}'.format(trackIndex, trackCollection))
        return collStrList

    # Temporary solution. Should be refactored to not make use of setReferenceTrackFileNames()
    # in Method classes.

    @classmethod
    def getTrackCollSpecFromCollStr(cls, collStr):
        if collStr:
            return [cls.PREBUILT] + collStr.split(': ')
        else:
            return [cls.PREBUILT]

    def isPartOfTrackCollSpec(self, trackFile):
        return trackFile == self.PREBUILT or \
               trackFile in self._trackIndex2CollectionReg or \
               trackFile in self._allCollections

    def isTrackCollSpec(self, trackFiles):
        return (len(trackFiles) == 1 and
                trackFiles[0] == self.PREBUILT) or \
               (len(trackFiles) == 3 and
                trackFiles[0] == self.PREBUILT and
                trackFiles[1] in self._trackIndex2CollectionReg and
                trackFiles[2] in self._allCollections)

    @staticmethod
    def getTrackIndexAndCollFromTrackCollSpec(trackFiles):
        if len(trackFiles) == 3:
            return trackFiles[1], trackFiles[2]
        else:
            return '', ''


refTrackCollRegistry = RefTrackCollectionRegistry()
