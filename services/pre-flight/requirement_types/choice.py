from .requirement_type import Requirement
from .requirement_with_children import RequirementWithChildren
from yattag import Doc

class Choice(Requirement):

    def __init__(self, name):
        super(Choice, self).__init__(name)
        self.options = []

    def get_html(self):
        return_string = ""+ self.name + ":<br /><br />"
        return_string += self.__build_options(self.name)
        return return_string

    def __build_options(self, name):
        doc, tag, text = Doc().tagtext()
        outer_stripped_name = name.replace(" ", "-")
        with tag('div', id=outer_stripped_name):
            for radio_option in self.options:

                stripped_name = self.name.replace(" ", "-")
                stripped_radio_name = radio_option.name.replace(" ", "-")

                choiceID = stripped_name+stripped_radio_name
                with tag('ul', klass='ul'):
                    with tag('li', klass='lines'):
                doc.asis("<input type=\"radio\" id=\""+choiceID+"\" name=\""+stripped_name+"\" onchange=\"changeVisibility('"+stripped_radio_name+"', '"+choiceID+"', '"+stripped_name+"')\"/>")
                        doc.asis("<label for=\""+choiceID+"\">"+radio_option.name+"</label>")
                        doc.asis("<div for=\""+choiceID+"\", class=\"choicebutton\"></div>")
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
            stripped_self_name = self.name.replace(" ", "-")
            stripped__name = name.replace(" ", "-")
            with tag('div', id=stripped_self_name, klass=stripped__name, style='display:none'):
                doc.asis(child.get_html() + "<br />")

