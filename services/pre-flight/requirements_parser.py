import re
regex = "(requirement)-([a-å]+)"


def parse_json(json):
    result_to_return = ""
    for key, child in json.items():
        result = re.match(regex, key, re.IGNORECASE)
        if result is not None:
            requirement = result.group(2)
            if __parse_requirement(requirement, child) == False:
                return "Der skete en fejl, requirementet: \"" + requirement + "\" kendes ikke."
            else:
                result_to_return += __parse_requirement(requirement, child) + "<br />"
        else:
            return "Der skete en fejl, law-template.json filen er ikke konfigureret korrekt! Et requirement skal hedde: \"requirement-[NAVN]\"."

    return result_to_return


def __parse_requirement(key, tree):
    if key == "radio":
        return __parse_radio(tree)
    elif key == "upload":
        return __parse_upload(tree)
    else:
        return False


def __parse_radio(tree):
    return_string = ""
    for key, child in tree.items():
        print("Tree key: " + key)
        return_string += key + "\n"
    return "Radio buttons: " + return_string


def __parse_upload(requirement):
    print(requirement['name'])
    return "Upload field: " + requirement['name']
