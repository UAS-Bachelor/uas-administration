from .requirement_type import Requirement
from yattag import Doc

class Multiline_text(Requirement):

    def __init__(self, name):
        super(Multiline_text, self).__init__(name)
        self.default_value = ""

    def set_default_value(self, value):
        self.default_value = value

    def get_html(self):
        doc, tag, text = Doc().tagtext()
        with tag('div'):
            text(self.name)
            stripped_name = self.name.replace(" ", "-")
            doc.asis("<br/>")
            with tag('textarea', rows='10', cols='100', klass='comment', id='multiline-'+stripped_name, name='multiline',placeholder='Write comment here if you are ugly as f*ck lmao...'):
                pass
        return doc.getvalue()