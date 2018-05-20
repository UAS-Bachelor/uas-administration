import xml.etree.ElementTree as ET
import re

from exceptions.requirement_choice_exception import WrongChoiceChildException
from exceptions.requirement_exception import RequirementNotRecognized
from exceptions.requirement_map_exception import NoSafetyZoneOnMapException, MapNotChildOfRoot
from exceptions.root_exception import WrongRootException
from exceptions.tag_name_exception import NoNameException, EmptyNameException
from requirement_types.checkbox import Checkbox
from requirement_types.supply_file import SupplyFile
from requirement_types.choice import Choice, Option
from requirement_types.root import Root
from requirement_types.map import Map
from requirement_types.text import Text
from requirement_types.multiline_text import MultilineText
from yattag import Doc 

__regex = "(requirement)-(.+)"
__error = False
__error_msg = "Something went wrong."


def load_xml(path):
    global __error
    __error = False

    node_root = Root("Root")

    tree = ET.parse(path)
    root = tree.getroot()
    if not root.tag == "requirements":
        raise WrongRootException()
    parse_childs(root, node_root)

    if __error:
        return __error_msg
    return build_html(node_root)


def build_html(root):
    doc, tag, text = Doc().tagtext()
    root_id = "root-form"
    with tag('form', name='overall', id=root_id):
        for node in root.get_children():
            doc.asis(node.get_html() + "<br />")
        doc.stag('input', type="button", value="Create mission", onclick='validateSubmit("' + root_id + '")')

    return doc.getvalue()


def parse_childs(node, parent):
    for child in node:
        requirement = re.match(__regex, child.tag, re.IGNORECASE)

        if requirement is None:
            raise RequirementNotRecognized(child.tag)
            #set_error("The requirement tag: \"" + child.tag + "\" is not recognized.")
        else:
            requirement_type = requirement.group(2)

            if requirement_type == "supply-file":
                parse_supply_file(child, parent)

            elif requirement_type == "choice":
                parse_choice(child, parent)

            elif requirement_type == "map":
                parse_map(child, parent)

            elif requirement_type == "text":
                parse_text(child, parent)

            elif requirement_type == "checkbox":
                parse_checkbox(child, parent)

            elif requirement_type == "multiline-text":
                parse_multiline_text(child, parent)
            else:
                raise RequirementNotRecognized(requirement_type)
                #set_error("The requirement tag: \"" + requirement_type + "\" is not recognized.")


def parse_map(node, parent):
    if isinstance(parent, Root):
        if not name_tag_error(node, "Map"):
            if node.get('safetyzoneSize') is None:
                raise NoSafetyZoneOnMapException()
                #set_error("The map requirement must have a safety zone size!")
            else:
                new_map_requirement = Map(node.get('name'))
                new_map_requirement.set_safety_zone_size(node.get('safetyzoneSize'))
                parent.add_child(new_map_requirement)
    else:
        raise MapNotChildOfRoot(parent.name)
        #set_error("The map requirement can only be a child of root not \"" + parent.name + "\".") #Might wanna add type to object


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
                '''if len(option) == 0:
                    set_error("A choice can not have zero children!")
                else:'''
                parse_childs(option, new_option)

        else:
            raise WrongChoiceChildException(option.tag)
            #set_error("A choice requirement, can only consist of \"choice\" tags. Not \"" + option.tag + "\"")


def parse_supply_file(node, parent):
    if not name_tag_error(node, "Supply file"):
        new_supply_file_requirement = SupplyFile(node.get('name'))
        parent.add_child(new_supply_file_requirement)


def parse_text(node, parent):
    if not name_tag_error(node, "Text"):
        new_text_requirement = Text(node.get('name'))
        if "default" in node.attrib:
            new_text_requirement.set_default_value(node.get('default'))
        parent.add_child(new_text_requirement)


def parse_checkbox(node, parent):
    if not name_tag_error(node, "Checkbox"):
        new_checkbox_requirement = Checkbox(node.get('name'))
        parent.add_child(new_checkbox_requirement)
        parse_childs(node, new_checkbox_requirement)


def parse_multiline_text(node, parent):
    if not name_tag_error(node, "Multiline Text"):
        new_multiline_text_requirement = MultilineText(node.get('name'))
        parent.add_child(new_multiline_text_requirement)


def name_tag_error(node, requirement_type):
    if node.get('name') is None:
        #set_error("The " + requirement_type + " requirement, needs to have a name!")
        raise NoNameException(requirement_type)
        return True

    elif node.get('name') is "":
        #set_error("The " + requirement_type + " requirement, can not have an empty name field!")
        raise EmptyNameException(requirement_type)
        return True

    return False


def set_error(msg):
    global __error_msg, __error
    __error = True
    __error_msg = msg
