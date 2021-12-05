class Student:
    def __init__(self, stid, fname, lname, gpa):
        self.stid = stid
        self.fname = fname
        self.lname = lname
        self.gpa = gpa

#Returns a welcome message addressing the user
def getWelcomeMessage(username):
    #Username is a string
    return "Welcome back, " + username
