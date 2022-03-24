from __future__ import absolute_import, division, print_function, unicode_literals

__metaclass__ = type


CONFIG_SECTION = u'pycolocstats'
DEFAULT_CONFIG_REL_FN = '.pycolocstats/pycolocstats.ini'
SAMPLE_CONFIG_REL_FN = 'config/pycolocstats.ini.sample'


def getConfigParser(config_fn):
    from configparser import ConfigParser
    cfgParser = ConfigParser()
    cfgParser.read(config_fn)
    assert len(cfgParser.sections()) == 1 and cfgParser.sections()[0] == CONFIG_SECTION
    return cfgParser


def getConfigFilename():
    import os
    import pkg_resources
    import shutil

    sampleConfigFn = pkg_resources.resource_filename('pycolocstats', SAMPLE_CONFIG_REL_FN)

    envConfigFn = os.environ.get('PYCOLOCSTATS_CONFIG')
    configFn = envConfigFn if envConfigFn else DEFAULT_CONFIG_REL_FN

    if not os.path.exists(configFn):
        print("Writing config file: " + configFn)
        os.makedirs(os.path.dirname(configFn))
        shutil.copy(sampleConfigFn, configFn)
    else:
        sampleCfgParser = getConfigParser(sampleConfigFn)
        cfgParser = getConfigParser(configFn)

        if set(sampleCfgParser[CONFIG_SECTION].keys()) != set(cfgParser[CONFIG_SECTION].keys()):
            sampleCfgParser.read(configFn)
            with open(configFn, 'w') as configFile:
               sampleCfgParser.write(configFile)

    return configFn


cfgParser = getConfigParser(getConfigFilename())

CATCH_METHOD_EXCEPTIONS = cfgParser.getboolean(CONFIG_SECTION, 'catch_method_exceptions')
VERBOSE_RUNNING = cfgParser.getboolean(CONFIG_SECTION, 'verbose_running')
TMP_DIR = cfgParser.get(CONFIG_SECTION, 'tmp_dir')
DEFAULT_JOB_OUTPUT_DIR = cfgParser.get(CONFIG_SECTION, 'default_job_output_dir')
PULL_DOCKER_IMAGES = cfgParser.getboolean(CONFIG_SECTION, 'pull_docker_images')
USE_TEST_DOCKER_IMAGES = cfgParser.getboolean(CONFIG_SECTION, 'use_test_docker_images')
REF_COLL_GSUITES_PATH = cfgParser.get(CONFIG_SECTION, 'ref_coll_gsuites_path')
ENABLE_METHODS_PARALLELISATION = cfgParser.getboolean(CONFIG_SECTION, 'enable_methods_parallelisation')
MAX_PARALLEL_METHODS = cfgParser.getint(CONFIG_SECTION, 'max_parallel_methods')
ENABLE_JOBS_PARALLELISATION = cfgParser.getboolean(CONFIG_SECTION, 'enable_jobs_parallelisation')
MAX_PARALLEL_JOBS = cfgParser.getint(CONFIG_SECTION, 'max_parallel_jobs')
