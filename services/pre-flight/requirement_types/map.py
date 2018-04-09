from .requirement_type import Requirement


class Map(Requirement):

    def __init__(self, name):
        super(Map, self).__init__(name)

    def get_html(self):
        return "Map requirement: <br />Name: " + self.name + "<br />"
