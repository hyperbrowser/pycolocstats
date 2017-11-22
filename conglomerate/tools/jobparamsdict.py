import os

from conglomerate.tools.types import PathStr, PathStrList


class JobParamsDict(dict):
    def __init__(self, paramDefDict):
        super(JobParamsDict, self).__init__(self)
        self._paramDefDict = paramDefDict

    def __setitem__(self, key, val):
        assert key in self.getAllowedKeys(), '"{}" not in allowed keys: {}'.format(key,
                                                                                   ', '.join(self.getAllowedKeys()))

        allowedType = self.getType(key)
        if allowedType == PathStr:
            assert isinstance(val, str), '"{}" not of correct type: {}'.format(val, str)
            assert os.path.exists(val), 'File "{}" does not exist'.format(val)
            val = {'class': 'File', 'location': val}
        elif allowedType == PathStrList:
            assert isinstance(val, list), '"{}" not of correct type: {}'.format(val, list)
            assert all(isinstance(f, str) for f in val), 'Some of {} entries are not of correct type: {}'.format(val,
                                                                                                                 str)
            assert all(os.path.exists(f) for f in val), 'Some of "{}" does not exist'.format(val)
            val = [{'class': 'File', 'location': f} for f in val]
        else:
            assert isinstance(val, allowedType), '"{}" not of correct type: {}'.format(val, allowedType)
        super(JobParamsDict, self).__setitem__(key, val)

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
