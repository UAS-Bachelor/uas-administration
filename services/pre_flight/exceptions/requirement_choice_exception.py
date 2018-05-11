class WrongChoiceChildException(Exception):

    def __init__(self, requirement):
        self.message = "A choice requirement, can only consist of \"choice\" tags. Not \"" + requirement + "\""
        super().__init__(self.message)
