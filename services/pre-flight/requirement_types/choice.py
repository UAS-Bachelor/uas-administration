from .requirement_type import Requirement


class Choice(Requirement):

    def __init__(self, name):
        super(Choice, self).__init__(name)
        self.options = []
        self.node = name

    def get_html(self):
        return_string = "Choice requirement: <br />Name: " + self.name + "<br /><br />"
        return_string += self.__build_options()
        return return_string

    def __build_options(self):
        return_string = ""
        for option in self.options:
            return_string += option.build_html()
        return return_string

    def add_option(self, option):
        self.options.append(option)


class Option:

    def __init__(self, name):
        self.child_list = []
        self.name = name

    def add_child(self, child):
        self.child_list.append(child)

    def get_children(self):
        return self.child_list

    def build_html(self):
        return_string = "Choice option: " + self.name + " at size: {0}".format(len(self.child_list))
        return_string += "<br />"
        for child in self.child_list:
            return_string += child.get_html() + "<br />"
        return return_string
