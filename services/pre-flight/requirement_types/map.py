from yattag import Doc

from .requirement_type import Requirement
from flask import render_template


class Map(Requirement):

    def __init__(self, name):
        super(Map, self).__init__(name)

    def set_safety_zone_size(self, size):
        self.safety_zone_size = size

    def get_html(self):
        doc, tag, text = Doc().tagtext()

        with tag('div', id='map-requirement', style='display:none'):
            result = render_template('open_layers_map.html', bufferSize=self.safety_zone_size)
            stripped_name = self.name.replace(" ", "-")
            doc.asis('<p></p>')
            doc.stag('input', type='file', id='map-overlap-' + stripped_name, name=stripped_name)

        result += doc.getvalue()
        return result
