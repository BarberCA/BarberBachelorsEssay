from os import name


def returnsExpectedTemplate(funcTree, attrSet):
    attrStatement = getAttrStatement(attrSet)
    argLen = len(funcTree['args']['args'])
    args = ""
    argList = ""
    for i in range(argLen):
        argName = funcTree['args']['args'][i]['arg'].capitalize()
        d = {'i':i, 'argName':argName}
        newArg = "\n    test{argName} = CREATE_{argName}{i}".format(**d)
        args += newArg
        argList += ", test{argName}".format(argName = argName)
    if len(argList) != 0:
        argList = argList[2:]
    s = """{attrStatement}def assert():{args}
    result = {functionName}({argList})
    assert result == EXPECTED_RESULT"""
    d = {
        'attrStatement':attrStatement,
        'args':args,
        'argList':argList,
        'functionName':funcTree['name'],
        'target':funcTree['name'][3:]
    }
    template = s.format(**d)
    return template


def getAttrStatement(attrSet):
    return "The input variables should have the following attributes: " + str(attrSet) + "\n"
