from .requirement_type import Requirement
from yattag import Doc


class Text(Requirement):

    def __init__(self, name):
        super(Text, self).__init__(name)

    def get_html(self):
        doc, tag, text = Doc().tagtext()
        with tag('div'):
            text(self.name)
            stripped_name = self.name.replace(" ", "-")
            doc.stag('input', type='text', id='upload-file-'+stripped_name, name=stripped_name)
        return doc.getvalue()
