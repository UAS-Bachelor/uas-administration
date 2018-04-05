import xml.etree.ElementTree as ET
import re
from requirement_types.supply_file import SupplyFile
from requirement_types.choice import Choice

regex = "(requirement)-(.+)"
error = False
error_msg = "Something went wrong."


def load_xml(path):
    global error
    error = False

    tree = ET.parse(path)
    root = tree.getroot()
    childs = parse_childs(root)

    if error:
        return error_msg
    return build_html(childs)


def build_html(nodes):
    return_string = ""
    for node in nodes:
        return_string += node.get_html() + "<br /><br />"

    return return_string


def parse_childs(root):
    requirements = []
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
            error = True
            error_msg = "The requirement tag: \"" + requirement_type + "\" is not recognized."
    return requirements


def parse_choice(child):
    global error, error_msg
    if not name_tag_error(child):
        new_choice_requirement = Choice(child)
        return new_choice_requirement


def parse_supply_file(child):
    global error, error_msg
    if not name_tag_error(child):
        new_supply_file_requirement = SupplyFile(child)
        return new_supply_file_requirement


def name_tag_error(node):
    global error_msg, error
    if node.get('name') is None:
        error = True
        error_msg = "The supply file element, needs to have a name!"
        return True

    elif node.get('name') is "":
        error = True
        error_msg = "The supply file element, can not have an empty field"
        return True

    return False
