from conglomerate.tools.util import deleteAllTmpFiles


def runAllMethodsInSequence(methods):
    for method in methods:
        resultFilesDict = method.createJob().run()
        method.setResultFilesDict(resultFilesDict)
    deleteAllTmpFiles()
