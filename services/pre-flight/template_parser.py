import xml.etree.ElementTree as ET
import re
from requirement_types.supply_file import SupplyFile
from requirement_types.choice import Choice, Option
from requirement_types.root import Root

__regex = "(requirement)-(.+)"
__error = False
__error_msg = "Something went wrong."


def load_xml(path):
    global __error
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
    for child in node:
        requirement = re.match(__regex, child.tag, re.IGNORECASE)
        requirement_type = requirement.group(2)

        if requirement_type == "supply-file":
            parse_supply_file(child, parent)

        elif requirement_type == "choice":
            parse_choice(child, parent)

        else:
            global __error, __error_msg
            set_error("The requirement tag: \"" + requirement_type + "\" is not recognized.")


def parse_choice(node, parent):
    if not name_tag_error(node, "Choice"):
        new_choice_requirement = Choice(node.get('name'))
        parent.add_child(new_choice_requirement)
        parse_choice_option(node, new_choice_requirement)


def parse_choice_option(node, parent_choice):
    for option in node:
        if option.tag == "choice":
            if not name_tag_error(option, "Choice option"):
                new_option = Option(option.get('name'))
                parent_choice.add_option(new_option)
                parse_childs(option, new_option)

        else:
            set_error("A choice requirement, can only consist of \"choice\" tags. Not \"" + option.tag + "\"")


def parse_supply_file(node, parent):
    if not name_tag_error(node, "Supply file"):
        new_supply_file_requirement = SupplyFile(node.get('name'))
        parent.add_child(new_supply_file_requirement)


def name_tag_error(node, requirement_type):
    if node.get('name') is None:
        set_error("The " + requirement_type + " requirement, needs to have a name!")
        return True

    elif node.get('name') is "":
        set_error("The " + requirement_type + " requirement, can not have an empty name field!")
        return True

    return False


def set_error(msg):
    global __error_msg, __error
    __error = True
    __error_msg = msg
