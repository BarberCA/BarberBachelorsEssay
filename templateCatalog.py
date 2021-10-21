from os import name


def returnsExpectedTemplate(funcTree, argIDs, argTypes, argAttributes):
    attrStatement = getAttrStatement(argIDs, argTypes, argAttributes)
    argLen = len(funcTree['args']['args'])
    args = ""
    argList = ""
    for i in range(argLen):
        argName = funcTree['args']['args'][i]['arg']
        d = {'i':i, 'argName':argName}
        newArg = "\n    {argName} = CREATE_{argName}{i}".format(**d)
        args += newArg
        argList += ", {argName}".format(argName = argName)
    if len(argList) != 0:
        argList = argList[2:]
    s = """{attrStatement}def assert{capFuncName}ReturnsExpected():{args}
    result = {functionName}({argList})
    assert result == EXPECTED_RESULT"""
    d = {
        'attrStatement':attrStatement,
        'args':args,
        'argList':argList,
        'functionName':funcTree['name'],
        'capFuncName':funcTree['name'].capitalize(),
        'target':funcTree['name'][3:]
    }
    template = s.format(**d)
    return template


def getAttrStatement(argIDs, argTypes, argAttributes):
    if not argIDs:
        statement = "There are no arguments for this test."
    else:
        statement = "TEST HAS THE FOLLOWING INPUT VARIABLES:\n"
        argIDs = list(argIDs)
        for i in range(len(argIDs)):
            attrs = str(list(argAttributes[i]))
            statement = statement + "    '%s' is of type '%s', with attributes %s\n" % (argIDs[i], argTypes[i], attrs)
    return statement