import os
from tempfile import mkstemp

TMP_FILENAME_STORAGE = []


def getTemporaryFileName(suffix='.bed'):
    tmpFileName = mkstemp(suffix=suffix, dir='/tmp')[1]
    TMP_FILENAME_STORAGE.append(tmpFileName)
    return tmpFileName


def deleteAllTmpFiles():
    while TMP_FILENAME_STORAGE:
        os.unlink(TMP_FILENAME_STORAGE.pop())
