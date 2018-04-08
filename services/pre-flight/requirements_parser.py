import re

regex = "(requirement)-([a-å]+)"
__error = False


def parse_json(json):
    result_to_return = ""
    for key, child in json.items():
        result = re.match(regex, key, re.IGNORECASE)
        if result is not None:
            requirement = result.group(2)
            parse_result = __parse_requirement(requirement, child)
            if not parse_result[0]:
                return parse_result[1]
            else:
                result_to_return += parse_result[1] + "<br />"
        else:
            return "Der skete en fejl, law-template.json filen er ikke konfigureret korrekt! " \
                   "Et requirement skal hedde: \"requirement-[NAVN]\"."

    return result_to_return


def __parse_requirement(key, tree):
    if key == "radio":
        return __parse_radio(tree)
    elif key == "upload":
        return __parse_upload(tree)
    else:
        return False, "Der skete en fejl, requirementet: \"" + key + "\" kendes ikke."


def __parse_radio(tree):
    return_string = ""

    if "options" not in tree:
        return False, "Fejl i radio requirementet, intet \"options\"."

    if "name" not in tree:
        return False, "Fejl i radio requirement, intet \"name\"."

    options = tree['options'].items()
    for key, child in options:
        print("Tree key: " + key)
        return_string += "<br /> " + __parse_option(key, child)
        #return_string += key + "\n"
    return True, "Radio buttons: Name: " + tree['name'] + "<br />" + return_string + "<br />"


def __parse_option(option, tree):
    return_string = "Option for: " + option + " :: "
    for key, child in tree.items():
        result = re.match(regex, key, re.IGNORECASE)
        print(__parse_requirement(result.group(2), child))
        return_string += __parse_requirement(result.group(2), child)[1]
    return return_string


def __parse_upload(requirement):
    if "name" not in requirement:
        return False, "Fejl i upload requirement, intet \"name\""

    print(requirement['name'])
    return True, "Upload field: " + requirement['name']
