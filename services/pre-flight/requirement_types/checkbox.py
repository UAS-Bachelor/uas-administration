from yattag import Doc

from requirement_types.requirement_with_children import RequirementWithChildren


class Checkbox(RequirementWithChildren):

    def __init__(self, name):
        super(Checkbox, self).__init__(name)

    def get_html(self):
        return_string = self.name
        return_string += self.__build_self(self.name)
        return return_string

    def __build_self(self, name):
        doc, tag, text = Doc().tagtext()
        outer_stripped_name = name.replace(" ", "-")
        with tag('div', id=outer_stripped_name):
            doc.asis(
                "<input type=\"checkbox\" name=\"" + outer_stripped_name + "\"/>")

        return doc.getvalue()
