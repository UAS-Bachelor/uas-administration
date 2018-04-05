from .requirement_type import Requirement


class Choice(Requirement):

    def __init__(self, node):
        super(Choice, self).__init__(node.get('name'))

    def get_html(self):
        return "Choice requirement: <br />Name: " + self.name
