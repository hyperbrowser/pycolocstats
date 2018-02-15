from __future__ import absolute_import, division, print_function, unicode_literals

__metaclass__ = type


CONFIG_SECTION = u'Conglomerate'
DEFAULT_CONFIG_REL_FN = '../config/conglomerate.ini'


def getConfigFilename():
    import os
    import pkg_resources
    import shutil

    envConfigFn = os.environ.get('CONGLOMERATE_CONFIG')
    if envConfigFn:
        return envConfigFn
    else:
        defConfigFn = pkg_resources.resource_filename('conglomerate', DEFAULT_CONFIG_REL_FN)
        if not os.path.exists(defConfigFn):
            sampleConfigFn = defConfigFn + '.sample'
            shutil.copy(sampleConfigFn, defConfigFn)
        return defConfigFn


def getConfigParser(config_fn):
    from configparser import ConfigParser
    cfgParser = ConfigParser()
    cfgParser.read(config_fn)
    assert len(cfgParser.sections()) == 1 and cfgParser.sections()[0] == CONFIG_SECTION
    return cfgParser


cfgParser = getConfigParser(getConfigFilename())

CATCH_METHOD_EXCEPTIONS = cfgParser.getboolean(CONFIG_SECTION, 'catch_method_exceptions')
VERBOSE_RUNNING = cfgParser.getboolean(CONFIG_SECTION, 'verbose_running')
