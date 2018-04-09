from .requirement_type import Requirement


class SupplyFile(Requirement):

    def __init__(self, name):
        super(SupplyFile, self).__init__(name)

    def get_html(self):
        return "Supply file requirement: <br />Name: " + self.name + "<br />"
