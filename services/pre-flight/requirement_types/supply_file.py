from .requirement_type import Requirement
from yattag import Doc

class SupplyFile(Requirement):

    def __init__(self, name):
        super(SupplyFile, self).__init__(name)

    def get_html(self):
        doc, tag, text = Doc().tagtext()
        with tag('div', klass='upload-div'):
            with tag('p', klass='upload-file'):
                text(self.name)
            stripped_name = self.name.replace(" ", "-")
            doc.stag('input', type='file', id='file', klass='inputfile', name=stripped_name)
            doc.asis("<label for=\"file\">Choose a file</label>")
        return doc.getvalue()
        
        #"Supply file requirement: <br />Name: " + self.name + "<br />"
