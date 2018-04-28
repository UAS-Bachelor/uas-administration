from .requirement_type import Requirement
from flask import render_template


class Map(Requirement):

    def __init__(self, name):
        super(Map, self).__init__(name)
        self.safety_zone_size = 0

    def set_safety_zone_size(self, size):
        self.safety_zone_size = size

    def get_html(self):
        return render_template('open-layers-map.html', bufferSize=self.safety_zone_size)
