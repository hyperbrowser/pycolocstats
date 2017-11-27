import os
from tempfile import mkstemp

TMP_FILENAME_STORAGE = []


def getTemporaryFileName(suffix='.bed'):
    tmpFileName = mkstemp(suffix=suffix, dir='/tmp')[1]
    TMP_FILENAME_STORAGE.append(tmpFileName)
    return tmpFileName


def deleteAllTmpFiles():
    for fn in TMP_FILENAME_STORAGE:
        os.unlink(fn)
