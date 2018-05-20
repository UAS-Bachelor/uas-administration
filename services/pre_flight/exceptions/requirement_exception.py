class RequirementNotRecognized(Exception):

    def __init__(self, requirement):
        self.message = "The requirement " + requirement + " is not recognized."
        super().__init__(self.message)
