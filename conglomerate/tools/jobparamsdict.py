import os

from conglomerate.tools.types import PathStr


class JobParamsDict(dict):
    def __init__(self, paramDefDict):
        super(JobParamsDict, self).__init__(self)
        self._paramDefDict = paramDefDict

    def __setitem__(self, key, val):
        assert key in self.getAllowedKeys(), \
            '"{}" not in allowed keys: {}'.format(key, ', '.join(self.getAllowedKeys()))

        allowedType = self.getType(key)
        if allowedType == PathStr:
            val = self._assert_and_format_path_type(val)
        else:
            assert isinstance(val, allowedType), \
                '"{}" not of correct type: {}'.format(val, allowedType)
        super(JobParamsDict, self).__setitem__(key, val)

    def _assert_and_format_path_type(self, val):
        assert isinstance(val, str), \
            '"{}" not of correct type: {}'.format(val, str)
        assert os.path.exists(val), \
            'File "{}" does not exist'.format(val)

        topDir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..')
        topDirRelPath = os.path.relpath(os.path.abspath(val), topDir)

        return {'class': 'File', 'location': topDirRelPath}

    def getAllowedKeys(self):
        return self._paramDefDict.keys()

    def getType(self, key):
        return self._paramDefDict[key]['type']

    def isMandatory(self, key):
        return self._paramDefDict[key]['mandatory']

    def isPresent(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def getAbsentMandatoryParameters(self):
        absentMandatoryParameters = []
        for key in self.getAllowedKeys():
            if self.isMandatory(key) and not self.isPresent(key):
                absentMandatoryParameters.append(key)
        return absentMandatoryParameters

    def __repr__(self):
        retStr = super(JobParamsDict, self).__repr__()
        retStr += '\nAllowed params:\n'
        for key in self.getAllowedKeys():
            retStr += '\t%s: %s %s\n' % (key, self.getType(key), '[x]' if self.isMandatory(key) else '[ ]')
        retStr += '[ ] for optional parameter, [x] for mandatory parameter'
        return retStr
