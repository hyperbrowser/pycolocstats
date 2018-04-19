from __future__ import absolute_import, division, print_function, unicode_literals

__metaclass__ = type


class MissingMandatoryParameters(Exception):
    def __init__(self, absentMandatoryParameters):
        super(MissingMandatoryParameters, self).__init__(
            'Missing mandatory parameters: %s' % ', '.join(absentMandatoryParameters))
        self.absentMandatoryParameters = absentMandatoryParameters


class AbstractMethodError(Exception):
    pass


class ShouldNotOccurError(Exception):
    pass
