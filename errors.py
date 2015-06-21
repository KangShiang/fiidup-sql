class Error(object):
    def __init__(self, error):
        self.error = error

    def message(self):
        return self.error
