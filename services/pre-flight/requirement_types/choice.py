from .requirement_type import Requirement


class Choice(Requirement):

    def __init__(self, name):
        super(Choice, self).__init__(name)
        self.node = name

    def get_html(self):
        return "Choice requirement: <br />Name: " + self.name


class Option:

    def __init__(self, name):
        self.name = name
