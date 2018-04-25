from .requirement_type import Requirement
from yattag import Doc


class Text(Requirement):

    def __init__(self, name):
        super(Text, self).__init__(name)
        self.default_value = ""

    def set_default_value(self, value):
        self.default_value = value

    def get_html(self):
        doc, tag, text = Doc().tagtext()
        with tag('div'):
            text(self.name)
            stripped_name = self.name.replace(" ", "-")

            doc.stag('input', type='text', id='upload-file-'+stripped_name, name=stripped_name, value=self.default_value)
        return doc.getvalue()
