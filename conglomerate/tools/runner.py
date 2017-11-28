from conglomerate.methods.multimethod import MultiMethod
from conglomerate.tools.util import deleteAllTmpFiles


def runAllMethodsInSequence(methods):
    try:
        for method in methods:
            jobs = method.createJobs()
            if len(jobs) == 1:
                job = jobs[0]
                resultFilesDict = job.run()
                method.setResultFilesDict(resultFilesDict)
            elif len(jobs) > 1:
                assert isinstance(method, MultiMethod)
                resultFilesDictList = [job.run() for job in jobs]
                method.setResultFilesDictList(resultFilesDictList)
            else:
                raise NotImplementedError()
    finally:
        deleteAllTmpFiles()
