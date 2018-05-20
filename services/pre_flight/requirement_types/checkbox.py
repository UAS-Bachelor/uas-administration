from yattag import Doc
from .requirement_with_children import RequirementWithChildren


class Checkbox(RequirementWithChildren):

    def __init__(self, name):
        super(Checkbox, self).__init__(name)

    def get_html(self):
        return_string = self.__build_self(self.name)
        return return_string

    def __build_self(self, name):
        doc, tag, text = Doc().tagtext()
        stripped_name = name.replace(" ", "-")
        div_id = stripped_name + "-div"
        children_div_id = stripped_name + "-children-div"
        with tag('div', id=div_id):
            doc.asis("<label for=\"" + stripped_name + "\">" + name + "</label>")
            doc.asis(
                "<input type=\"checkbox\" id=\"" + stripped_name + "\" name=\"" + stripped_name + "\" onchange=\"changeVisibilityCheckbox('" + children_div_id + "', '" + stripped_name + "')\"/>")

            with tag('div', id=children_div_id, style='display:none'):
                for child in self.get_children():
                    doc.asis(child.get_html() + "<br />")
        return doc.getvalue()
