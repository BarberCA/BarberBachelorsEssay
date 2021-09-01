#!/usr/bin/env python
'''
From http://code.activestate.com/recipes/578625-python-ast-to-xml/
Ryan Gonzalez, MIT licensed

2015-02-05 Robert Stewart <rstewart@izeni.com> "Simplify output schema for further parsing."
'''

import ast, re, sys
from xml.dom import minidom
from xml.etree.ElementTree import iselement

try:
    from xml.etree import cElementTree as etree
except:
    try:
        from lxml import etree
    except:
        from xml.etree import ElementTree as etree

def prettify(xml_string):
    reparsed = minidom.parseString(xml_string)
    return reparsed.toprettyxml(indent="  ") 

class ast2xml(ast.NodeVisitor):
    def __init__(self):
        super(ast.NodeVisitor, self).__init__()
        self.path = []
        self.root = etree.Element('ast')
        self.celement = self.root
        self.lname = 'module'
    def convert(self, tree):
        self.visit(tree)
        return etree.tostring(self.root)
    def generic_visit(self, node):
        self.path.append(type(node).__name__)
        ocelement = self.celement
        self.celement = etree.SubElement(self.celement, self.lname)
        self.celement.attrib.update({'_name': type(node).__name__})
        olname = self.lname
        self.lname = type(node).__name__
        for item in node.__dict__:
            self.lname = item
            if isinstance(getattr(node, item), ast.AST):
                self.generic_visit(getattr(node, item))
            elif isinstance(getattr(node, item), list):
                ocel2 = self.celement
                olname2 = self.lname
                self.celement = etree.SubElement(self.celement, self.lname)
                self.celement.attrib.update({'_name': '_list'})
                self.lname = '_list_element'
                [self.generic_visit(childnode) for childnode in getattr(node, item) if isinstance(childnode, (ast.AST, list))]
                self.celement = ocel2
                self.lname = olname2
            else:
                self.celement.attrib.update({item: str(getattr(node, item))})
        self.path.pop()
        self.celement = ocelement
        self.lname = olname

#How to do this to modify ast.return and such?
#class testClass:
#    def testMethod(self):
#        print("Hello")

def main():#C:/Users/Carson Barber/Documents/Work/School/Bachelor's Essay/test.py
    with open("test.py", 'r') as f:
        tree = ast.parse(f.read())
        res = ast2xml().convert(tree)
        fnc = tree.body[0]
        important_vars, condition_set = processCode(fnc.body, set())
        print("done")

def processCode (b, important_vars:set):
    all_conditions = []
    for obj in reversed(b):
        if isinstance(obj, ast.Return):
            newVars = processReturn(obj)
            important_vars.update(newVars)
        elif isinstance(obj, ast.Assign):
            processAssign(obj, important_vars)
        elif isinstance(obj, ast.If):
            [important_vars, new_conditions] = processIf(obj, important_vars)
            all_conditions += new_conditions
        else:
            print("Error, unknown object type")
    return important_vars, all_conditions

def processReturn(b):
    important_vars = set()
    if isinstance(b.value, ast.Name):
        important_vars.add(b.value.id)
    elif isinstance(b.value, ast.BinOp):
        if isinstance(b.value.left, ast.Name):
            important_vars.add(b.value.left.id)
        if isinstance(b.value.right, ast.Name):
            important_vars.add(b.value.right.id)
    return important_vars

def processAssign(b, important_vars:set):
    for i in range(len(b.targets)):
        if b.targets[i].id in important_vars:
            important_vars.remove(b.targets[i].id)
            if isinstance(b.value, ast.Constant): #Direct assigment to constant, e.g. a=5
                pass
            elif isinstance(b.value, ast.Name): #Direct assigment, e.g. a=5
                important_vars.add(b.value.id)
            elif isinstance(b.value, ast.BinOp): #Binary operation, e.g. a=b+5
                processBinOp(b.value, important_vars)
            
def processBinOp(bop, important_vars):
    if isinstance(bop.left, ast.Name):
        important_vars.add(bop.left.id)
    elif isinstance(bop.left, ast.BinOp):
        processBinOp(bop.left, important_vars)
    if isinstance(bop.right, ast.Name):
        important_vars.add(bop.right.id)
    elif isinstance(bop.right, ast.BinOp):
        processBinOp(bop.right, important_vars)

def processIf(b, important_vars:set):
    conditions = []#List of conditions generated in this if block
    #Process case where evaluates true
    ifCondition = Condition(b.test, True)
    bodyVars, bodyConditions = processCode(b.body, important_vars.copy())
    if len(bodyConditions) > 0: #If the body has conditions, apply the if condition accross those conditions
        for cnd in bodyConditions:
            if isinstance(cnd, list):
                cnd.append(ifCondition)
            else:
                cnd = [cnd, ifCondition]
            conditions.append(cnd)
    else: #If the body has no conditions, add the if condition as is
        conditions.append(ifCondition)
    ret_vars = bodyVars

    #Process case where evaluates false
    elseCondition = ifCondition.invert()
    if 'orelse' in b._fields: #Case where 'else' is present
        orElseVars, orElseCdns = processCode(b.orelse, important_vars.copy())
        ret_vars.update(orElseVars)
        if len(orElseCdns) > 0: #If the body has conditions, apply the else condition accross those conditions
            for cnd in orElseCdns:
                if isinstance(cnd, list):
                    cnd.append(elseCondition)
                else:
                    cnd = [cnd, elseCondition]
                conditions.append(cnd)
        else: #If the else body has no conditions, add the else condition as is
            conditions.append(elseCondition)
    else: #Case where no 'else' is present
        conditions.append(elseCondition)

    return(ret_vars, conditions)

class Condition:
    def __init__(self, tests, evaluates):
        self.tests = tests
        self.evaluates = evaluates
    def invert(self):
        return Condition(self.tests, not self.evaluates)

        

#all_conditions: list of sublists of condition objects that are provide test cases by unique combinations (e.g. test1 & test2, test & not test2, etc.)
#Condition: list of tests and whether they should evaluate to true or false that makes up an element of condition_set

#Each independent if statement adds a list of conditions to the condition set.

if __name__ == '__main__':
    main()