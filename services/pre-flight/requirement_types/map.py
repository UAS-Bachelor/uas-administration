from .requirement_type import Requirement
from flask import render_template


class Map(Requirement):

    def __init__(self, name):
        super(Map, self).__init__(name)

    def setSafetyzoneSize(self, size):
        self.safetyzoneSize = size

    def get_html(self):
        return render_template('open_layers_map.html', bufferSize=self.safetyzoneSize)
        #return "Map requirement: <br />Name: " + self.name + "<br />"
