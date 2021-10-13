#From a given json tree extract a test template
import templateCatalog as tcl
import json

def getTemplate(tree):
    templateID = getTemplateID(tree)
    return makeTemplate(templateID, tree)

#Find what template to use for a given tree
def getTemplateID(tree):
    return "returnsExpected"

#Returns a string representation of the template for the corresponding templateID
def makeTemplate(templateID, tree):
    attrSet = findAttributes('student', tree)
    template = {
        'returnsExpected':
            tcl.returnsExpectedTemplate(tree, attrSet)
    }[templateID]
    return template


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
