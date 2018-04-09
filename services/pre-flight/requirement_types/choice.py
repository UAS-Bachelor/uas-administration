from .requirement_type import Requirement
from .requirement_with_children import RequirementWithChildren
from yattag import Doc

class Choice(Requirement):

    def __init__(self, name):
        super(Choice, self).__init__(name)
        self.options = []

    def get_html(self):
        return_string = "Choice requirement: <br />Name: " + self.name + "<br /><br />"
        return_string += self.__build_options(self.name)
        return return_string

    def __build_options(self, name):
        return_string = ""
        for option in self.options:
            return_string += option.get_html(name)
        return return_string

    def add_option(self, option):
        self.options.append(option)


class Option(RequirementWithChildren):

    def __init__(self, name):
        super(Option, self).__init__(name)

    def get_html(self, name):
        doc, tag, text = Doc().tagtext()
        #return_string = "Choice option: " + self.name + " at size: {0}".format(len(self.get_children()))
        #return_string += "<br />"
        for child in self.get_children():
            #return_string += child.get_html() + "<br />"
            #doc.stag('input', type='radio', name=name, onclick=template.handleRadioButtons.test())
            doc.asis('<input type="radio" name="'+name+'" onclick=template.handleRadioButtons.test()/>')
            text(self.name)
            with tag('div', id='test', style='display:none'):
                doc.asis(child.get_html() + "<br />")
        return doc.getvalue()
