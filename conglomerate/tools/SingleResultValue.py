class SingleResultValue:
    def __init__(self, numericResult, textualResult):
        self.numericResult = numericResult
        self.textualResult = textualResult

    def __str__(self):
        return self.textualResult