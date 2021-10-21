class Student:
    def __init__(self, stid, fname, lname, gpa):
        self.stid = stid
        self.fname = fname
        self.lname = lname
        self.gpa = gpa

def getFullName(student):
    return student + ' ' + student.lname