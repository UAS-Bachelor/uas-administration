import xml.etree.ElementTree as ET
import re
from requirement_types.supply_file import SupplyFile
from requirement_types.choice import Choice, Option
from requirement_types.root import Root

regex = "(requirement)-(.+)"
__error = False
__error_msg = "Something went wrong."
requirements = []


def load_xml(path):
    global __error, requirements
    __error = False

    node_root = Root("Root")

    tree = ET.parse(path)
    root = tree.getroot()
    parse_childs(root, node_root)

    if __error:
        return __error_msg
    return build_html(node_root)


def build_html(root):
    return_string = ""
    for node in root.get_children():
        return_string += node.get_html() + "<br />"

    return return_string


def parse_childs(node, parent):
    global requirements
    for child in node:
        requirement = re.match(regex, child.tag, re.IGNORECASE)
        requirement_type = requirement.group(2)

        if requirement_type == "supply-file":
            parse_supply_file(child, parent)

        elif requirement_type == "choice":
            parse_choice(child, parent)

        else:
            global __error, __error_msg
            set_error("The requirement tag: \"" + requirement_type + "\" is not recognized.")
    return requirements


def parse_choice(node, parent):
    if not name_tag_error(node):
        new_choice_requirement = Choice(node.get('name'))
        parent.add_child(new_choice_requirement)
        parse_choice_option(node, new_choice_requirement)


def parse_choice_option(node, parent_choice):
    for option in node:
        if option.tag == "choice":
            new_option = Option(option.get('name'))
            parent_choice.add_option(new_option)
            #for child in option:
            #    print("reached!")
            #    print(new_option)
            #    print(child)
            parse_childs(option, new_option)

        else:
            set_error("A choice requirement, can only consist of \"choice\" tags. Not \"" + option.tag + "\"")


def parse_supply_file(node, parent):
    if not name_tag_error(node):
        new_supply_file_requirement = SupplyFile(node.get('name'))
        parent.add_child(new_supply_file_requirement)
        print(parent)


def name_tag_error(node):
    if node.get('name') is None:
        set_error("The supply file element, needs to have a name!")
        return True

    elif node.get('name') is "":
        set_error("The supply file element, can not have an empty field")
        return True

    return False


def set_error(msg):
    global __error_msg, __error
    __error = True
    __error_msg = msg
