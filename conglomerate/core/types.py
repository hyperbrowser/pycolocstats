from __future__ import absolute_import, division, print_function, unicode_literals

__metaclass__ = type


class PathStr(str):
    pass


class PathStrList(list):
    pass


class SingleResultValue(object):
    def __init__(self, numericResult, textualResult):
        self.numericResult = numericResult
        self.textualResult = textualResult

    def __str__(self):
        return self.textualResult


class TrackFile(object):
    def __init__(self, path, title):
        self.path = path
        self.title = title

    def __str__(self):
        return 'TrackFile(%s:%s)' % (str(self.title), str(self.path))