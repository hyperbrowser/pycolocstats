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

    def __repr__(self):
        return self.textualResult


class TrackFile(object):
    def __init__(self, path, title):
        assert path, 'Path missing for track %s' % title
        assert title, 'Path missing for track %s' % path
        self.path = path
        self.title = title

    def __repr__(self):
        return 'TrackFile(%s:%s)' % (str(self.title), str(self.path))