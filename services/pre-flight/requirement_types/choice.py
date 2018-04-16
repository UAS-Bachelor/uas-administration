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
        doc, tag, text = Doc().tagtext()
        
        for radio_option in self.options:
            choiceID = self.name+radio_option.name
            with tag('ul', klass='ul'):
                with tag('li', klass='lines'):
                    doc.asis("<input type=\"radio\" id=\""+choiceID+"\" name=\""+self.name+"\" class=\"choice\" onchange=\"changeVisibility('"+radio_option.name+"', '"+choiceID+"', '"+self.name+"')\"/>")
                    doc.asis("<label for=\""+choiceID+"\">"+radio_option.name+"</label>")
                    with tag('div', klass='choicebutton'):
                        pass
            #text(radio_option.name)
        for option in self.options:
            option.append_html(name, doc, tag, text)
        return doc.getvalue()

    def add_option(self, option):
        self.options.append(option)


class Option(RequirementWithChildren):
    
    def __init__(self, name):
        super(Option, self).__init__(name)

    def append_html(self, name, doc, tag, text):
        #return_string = "Choice option: " + self.name + " at size: {0}".format(len(self.get_children()))
        #return_string += "<br />"
        for child in self.get_children():
            with tag('div', id=self.name, klass=name, style='display:none'):
                doc.asis(child.get_html() + "<br />")

