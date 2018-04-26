from __future__ import absolute_import, division, print_function, unicode_literals
from concurrent.futures import ProcessPoolExecutor
import time

from pycolocstats.methods.multimethod import MultiMethod
from pycolocstats.core.config import (CATCH_METHOD_EXCEPTIONS,
                                      VERBOSE_RUNNING,
                                      DEFAULT_JOB_OUTPUT_DIR,
                                      ENABLE_METHODS_PARALLELISATION,
                                      ENABLE_JOBS_PARALLELISATION)
from pycolocstats.core.util import deleteAllTmpFiles

__metaclass__ = type


def runAllMethods(methods, jobOutputDir=DEFAULT_JOB_OUTPUT_DIR):
    try:
        if ENABLE_METHODS_PARALLELISATION and ENABLE_JOBS_PARALLELISATION:
            raise RuntimeError("enable_methods_parallelisation and enable_jobs_parallelisation should never be 'true' "
                               "at the same time!")
        if ENABLE_METHODS_PARALLELISATION:
            _runAllMethodsInParallel(methods, jobOutputDir)
        else:
            _runAllMethodsInSequence(methods, jobOutputDir)
    finally:
        deleteAllTmpFiles()


def _runAllMethodsInSequence(methods, jobOutputDir=DEFAULT_JOB_OUTPUT_DIR):
    for method in methods:
        _runMethod(method, jobOutputDir)


def _runAllMethodsInParallel(methods, jobOutputDir=DEFAULT_JOB_OUTPUT_DIR):
    with ProcessPoolExecutor(len(methods)) as pool:
        results = pool.map(_runMethodMultiArgs, [(method, jobOutputDir) for method in methods])
        for i, result in enumerate(results):
            if not isinstance(methods[i], MultiMethod):
                methods[i].setResultFilesDict(result.getResultFilesDict())
            else:
                methods[i].setResultFilesDictList(result.getResultFilesDictList())


def _runMethodMultiArgs(args):
    return _runMethod(*args)


def _runMethod(method, jobOutputDir):
    print('Running tool:', method._methodCls.__name__, '<br>')
    if VERBOSE_RUNNING:
        startTime = time.time()
        print('Running method:', str(method))
    try:
        jobs = method.createJobs(jobOutputDir)
    except Exception as e:
        if VERBOSE_RUNNING:
            print('Failing createJobs for: ', method)
        if not CATCH_METHOD_EXCEPTIONS:
            raise
        method.setRunSuccessStatus(False, 'Failing to create job: ' + str(e))
        return method
    if not isinstance(method, MultiMethod):
        assert len(jobs) == 1
        job = jobs[0]
        resultFilesDict = job.run()
        method.setResultFilesDict(resultFilesDict)
    else:
        # assert isinstance(method, MultiMethod)
        if ENABLE_JOBS_PARALLELISATION:
            with ProcessPoolExecutor(len(jobs)) as pool:
                features = [pool.submit(job.run) for job in jobs]
                pool.shutdown(wait=True)
            resultFilesDictList = [feature.result() for feature in features]
        else:
            resultFilesDictList = [job.run() for job in jobs]
        method.setResultFilesDictList(resultFilesDictList)
    if VERBOSE_RUNNING:
        print('Runtime: ', (time.time() - startTime) / 60.0, ' minutes')
    # else:
    #     raise NotImplementedError()
    return method
