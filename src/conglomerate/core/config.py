from __future__ import absolute_import, division, print_function, unicode_literals

__metaclass__ = type


CONFIG_SECTION = u'Conglomerate'
DEFAULT_CONFIG_REL_FN = '../config/conglomerate.ini'


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

    defConfigFn = pkg_resources.resource_filename('conglomerate', DEFAULT_CONFIG_REL_FN)
    sampleConfigFn = defConfigFn + '.sample'

    envConfigFn = os.environ.get('CONGLOMERATE_CONFIG')
    configFn = envConfigFn if envConfigFn else defConfigFn

    if not os.path.exists(configFn):
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
