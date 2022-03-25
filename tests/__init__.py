from inspect import getsourcefile
from os.path import abspath, dirname


def get_abspath_of_executed_file():
    return abspath(getsourcefile(lambda: 0))


TEST_RESOURCES_DIR = dirname(get_abspath_of_executed_file()) + '/resources'
