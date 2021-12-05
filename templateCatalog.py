from os import name

def returnsExpectedTemplate(funcTree, comments, argIDs, argTypes, argAttributes):
    attrStatement = getAttrStatement(argIDs, argTypes, argAttributes)
    commentStatement = getCommentStatement(comments)
    argLen = len(funcTree['args']['args'])
    args = ""
    argList = ""
    for i in range(argLen):
        argName = funcTree['args']['args'][i]['arg']
        d = {'argName':argName}
        newArg = "\n    {argName} = ...{argName}...".format(**d)
        args += newArg
        argList += ", {argName}".format(argName = argName)
    if len(argList) != 0:
        argList = argList[2:]
    s = """{attrStatement}{commentStatement}def assert{capFuncName}ReturnsExpected():{args}
    result = {functionName}({argList})
    assert result == ...EXPECTED_RESULT..."""
    d = {
        'attrStatement':attrStatement,
        'commentStatement':commentStatement,
        'args':args,
        'argList':argList,
        'functionName':funcTree['name'],
        'capFuncName':funcTree['name'][0].upper()+funcTree['name'][1:],
        'target':funcTree['name'][3:]
    }
    template = s.format(**d)
    return template


def getAttrStatement(argIDs, argTypes, argAttributes):
    statement = "'...' indicates placeholder values.\n"
    if not argIDs:
        statement = statement + "There are no arguments for this test.\n"
    else:
        statement = statement + "TEST HAS THE FOLLOWING INPUT VARIABLES:\n"
        argIDs = list(argIDs)
        for i in range(len(argIDs)):
            attrs = str(list(argAttributes[i]))
            statement = statement + "    '%s' is of type '%s', with attributes %s\n" % (argIDs[i], argTypes[i], attrs)
    return statement

def getCommentStatement(comments):
    if comments:
        out = "Found the following comments:\n"
        for c in comments:
            out = out + c + "\n"
    else:
        out = "No comments found for this method.\n"
    return out