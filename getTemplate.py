#From a given json tree extract a test template
import templateCatalog as tcl
import json

def getTemplate(tree):
    templateID = getTemplateID(tree)
    argIDs = getArgumentIDs(tree)
    argTypes = list()
    argAttributes = list()
    for a in argIDs:#Only does the last argument at the moment
        argType = getArgType(a, tree)
        if not argType:
            argType = "Unknown"
        argTypes.append(argType)
        attrSet = findAttributes(a, tree)
        argAttributes.append(attrSet)
    template = {
        'returnsExpected':
            tcl.returnsExpectedTemplate(tree, argIDs, argTypes, argAttributes)
    }[templateID]
    return template

#Find what template to use for a given tree
def getTemplateID(tree):
    return "returnsExpected"
    

#Finds the id of all arguments of the tree
def getArgumentIDs(tree):
    argIDs = set()
    subtree = tree.get('args').get('args')
    if subtree: #Check if arguments are empty
        for i in range(len(subtree)):
            argIDs.add(subtree[i].get('arg'))
    return argIDs

#Identifies any attributes id uses in the tree.
def findAttributes(id, tree):
    attributes = set()
    if isinstance(tree, list):
        for element in range(len(tree)):
            attributes = set.union(findAttributes(id, tree[element]), attributes)
    elif isinstance(tree, dict):
        if tree.get('_type') == 'Attribute':
            if tree.get('value').get('id') == id:
                attributes.add(tree.get('attr'))
        for element in tree:
            attributes = set.union(findAttributes(id, tree[element]), attributes)

    return attributes

#Attempts to infer the argument type of the input argID in the input tree
def getArgType(argID, tree):
    #List case, look at all elements of the list
    if isinstance(tree, list):
        for index in range(len(tree)):
            childArgType = getArgType(argID, tree[index])
            if childArgType:#Argument type found
                return childArgType
    #Dict case, check if BinOp and argID in BinOp, then see if the type can be
    #determined in the BinOp. Otherwise, look at all the elements of the tree
    elif isinstance(tree, dict):
        if tree.get('_type') == 'BinOp' and idInBinOp(tree, argID):
            binOpArgType = getBinOpArgType(tree)
            if binOpArgType:
                return binOpArgType
        for element in tree:
            childArgType = getArgType(argID, tree.get(element))
            if childArgType:#Argument type found
                return childArgType
    return ""

#Returns true if the given ID exists as a left or right value for the input BinOp
def idInBinOp(tree, id):
    for branch in ['left', 'right']:
        branchType = tree.get(branch).get('_type')
        if branchType == 'Name' and tree.get(branch).get('id') == id:
            return True
        if branchType == 'BinOp':
            branchResult = idInBinOp(tree.get(branch), id)
            if branchResult:
                return True
    return False

#Returns the type of any constant in the given binOp. Returns an empty string if unable to tell
def getBinOpArgType(tree):
    for branch in ['left', 'right']:
        branchType = tree.get(branch).get('_type')
        if branchType == 'Constant':
            return type(tree.get(branch).get('value')).__name__
        if branchType == 'BinOp':
            branchResult = getBinOpArgType(tree.get(branch))
            if branchResult:
                return branchResult
    return ""
        
        
