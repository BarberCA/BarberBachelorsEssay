#!/usr/bin/env python
'''
From http://code.activestate.com/recipes/578625-python-ast-to-xml/
Ryan Gonzalez, MIT licensed

2015-02-05 Robert Stewart <rstewart@izeni.com> "Simplify output schema for further parsing."
'''

import ast
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

