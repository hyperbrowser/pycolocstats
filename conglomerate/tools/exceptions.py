class MissingMandatoryParameters(Exception):
    def __init__(self, absentMandatoryParameters):
        super(MissingMandatoryParameters, self).__init__(
            'Missing mandatory parameters: %s' % ', '.join(absentMandatoryParameters))
        self.absentMandatoryParameters = absentMandatoryParameters
