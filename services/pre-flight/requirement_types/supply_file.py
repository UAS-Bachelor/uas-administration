from .requirement_type import Requirement


class SupplyFile(Requirement):

    def __init__(self, node):
        super(SupplyFile, self).__init__(node.get('name'))

    def get_html(self):
        return "Supply file requirement: <br />Name: " + self.name
