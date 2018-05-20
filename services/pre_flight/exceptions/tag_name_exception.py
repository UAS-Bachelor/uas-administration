class NoNameException(Exception):

    def __init__(self, requirement):
        self.message = "The requirement " + requirement + " does not have an name tag."
        super().__init__(self.message)


class EmptyNameException(Exception):
    def __init__(self, requirement):
        self.message = "The requirement " + requirement + " have an empty name tag."
        super().__init__(self.message)
