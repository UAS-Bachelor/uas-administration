from .requirement_type import Requirement
from yattag import Doc

class SupplyFile(Requirement):

    def __init__(self, name):
        super(SupplyFile, self).__init__(name)

    def get_html(self):
        doc, tag, text = Doc().tagtext()
        with tag('div'):
            text(self.name)
            doc.stag('input', type='file', name='upload-file')
        return doc.getvalue()
        
        #"Supply file requirement: <br />Name: " + self.name + "<br />"
