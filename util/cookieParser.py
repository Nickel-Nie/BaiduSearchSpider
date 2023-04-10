def cookie_parser(filename):
    cookieDict = {}
    with open(filename, "r") as f:
        cookieStr = f.read()

        for item in cookieStr.split(";"):
            item = item.strip()
            kv = item.split("=", 1)
            cookieDict[kv[0]] = kv[1]

    return cookieDict


def param_parser(filename):
    paramDict = {}
    with open(filename, "r") as f:
        content = f.readlines()
        for item in content:
            kv = item.split(":", 1)
            paramDict[kv[0].strip()] = kv[1].strip()
    return paramDict
