def parseJSON(json):
    for key, child in json.items():
        # print("Key " + key)
        print(key)
        print(key[:11])
        if (key[:12]) == "requirement-":
            return parseRequirement(key[12:], child)
        else:
            return "Der skete en fejl, law-template.json filen er ikke konfigureret korrekt!"
        # print(child)


def parseRequirement(key, tree):
    print(key)
    requirementTypes = {
        "radio": parseRadio(tree),
        "upload": ""
    }
    return requirementTypes.get(key, "Fejl")

def parseRadio(tree):
    print(tree)
    returnString = ""
    for key, child in tree.items():
        print(key)
        returnString += key + "\n"
    return returnString

