import xml.etree.ElementTree as ET
import re
from requirement_types.supply_file import SupplyFile
from requirement_types.choice import Choice, Option

regex = "(requirement)-(.+)"
error = False
error_msg = "Something went wrong."
requirements = []


def load_xml(path):
    global error, requirements
    error = False

    tree = ET.parse(path)
    root = tree.getroot()
    childs = parse_childs(root)

    if error:
        return error_msg
    return build_html(requirements)


def build_html(nodes):
    return_string = ""
    for node in nodes:
        return_string += node.get_html() + "<br /><br />"

    return return_string


def parse_childs(root):
    global requirements
    for child in root:
        requirement = re.match(regex, child.tag, re.IGNORECASE)
        requirement_type = requirement.group(2)

        if requirement_type == "supply-file":
            new_requirement = parse_supply_file(child)
            if new_requirement is not None:
                requirements.append(new_requirement)

        elif requirement_type == "choice":
            new_requirement = parse_choice(child)
            if new_requirement is not None:
                requirements.append(new_requirement)

        else:
            global error, error_msg
            set_error("The requirement tag: \"" + requirement_type + "\" is not recognized.")
    return requirements


def parse_choice(node):
    if not name_tag_error(node):
        new_choice_requirement = Choice(node.get('name'))
        parse_choice_option(node)
        return new_choice_requirement


def parse_choice_option(node):
    for option in node:
        if option.tag == "choice":
            new_option = Option(option.get('name'))
            print(new_option.name)
            for child in option:
                parse_childs(child)

        else:
            set_error("A choice requirement, can only consist of \"choice\" tags. Not \"" + option.tag + "\"")


def parse_supply_file(node):
    if not name_tag_error(node):
        new_supply_file_requirement = SupplyFile(node.get('name'))
        return new_supply_file_requirement


def name_tag_error(node):
    if node.get('name') is None:
        set_error("The supply file element, needs to have a name!")
        return True

    elif node.get('name') is "":
        set_error("The supply file element, can not have an empty field")
        return True

    return False


def set_error(msg):
    global error_msg, error
    error = True
    error_msg = msg
