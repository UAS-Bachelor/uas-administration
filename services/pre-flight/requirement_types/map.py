from .requirement_type import Requirement
from flask import render_template


class Map(Requirement):

    def __init__(self, name):
        super(Map, self).__init__(name)

    def set_safety_zone_size(self, size):
        self.safety_zone_size = size

    def get_html(self):
        return render_template('open_layers_map.html', bufferSize=self.safety_zone_size)
        #return "Map requirement: <br />Name: " + self.name + "<br />"
