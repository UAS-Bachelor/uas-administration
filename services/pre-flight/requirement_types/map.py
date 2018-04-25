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
        stripped_name = self.name.replace(" ", "-")

        with tag('div', name=stripped_name, id='map-requirement', style='display:none'):
            result = render_template('open_layers_map.html', bufferSize=self.safety_zone_size)

            doc.asis('<p></p>')
            with tag('div'):
                doc.stag('input', type='file', id='map-overlap-' + stripped_name, name="No flight requirement")

        result += doc.getvalue()
        return result
