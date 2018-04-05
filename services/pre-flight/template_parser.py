import xml.etree.ElementTree as ET
import re
from requirement_types.supply_file import SupplyFile

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
            parse_choice(child)

        else:
            global error, error_msg
            error = True
            error_msg = "The requirement tag: \"" + requirement_type + "\" is not recognized."
    return requirements


def parse_choice(child):
    pass


def parse_supply_file(child):
    global error, error_msg

    if child.get('name') is None:
        error = True
        error_msg = "The supply file element, needs to have a name!"

    elif child.get('name') is "":
        error = True
        error_msg = "The supply file element, can not have an empty field"

    else:
        new_supply_file_requirement = SupplyFile(child.get('name'))
        return new_supply_file_requirement
