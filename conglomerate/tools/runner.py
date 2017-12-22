from __future__ import absolute_import, division, print_function, unicode_literals

from conglomerate.methods.multimethod import MultiMethod
from conglomerate.tools.constants import CATCH_METHOD_EXCEPTIONS, VERBOSE_RUNNING
from conglomerate.tools.util import deleteAllTmpFiles

__metaclass__ = type


def runAllMethodsInSequence(methods):
    try:
        for method in methods:
            print('Temp1: ', str(method))
            try:
                jobs = method.createJobs()
            except Exception, e:
                if VERBOSE_RUNNING:
                    print('Failing createJobs for: ', method)
                if not CATCH_METHOD_EXCEPTIONS:
                    raise
                method.setRunSuccessStatus(False, 'Failing to create job: '+str(e))
                continue
            if not isinstance(method, MultiMethod):
                assert len(jobs) == 1
                job = jobs[0]
                resultFilesDict = job.run()
                method.setResultFilesDict(resultFilesDict)
            else:
                #assert isinstance(method, MultiMethod)
                resultFilesDictList = [job.run() for job in jobs]
                method.setResultFilesDictList(resultFilesDictList)
            # else:
            #     raise NotImplementedError()
    finally:
        deleteAllTmpFiles()
