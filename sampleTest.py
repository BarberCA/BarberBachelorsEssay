from sampleCode import Student, getFullName

def testGetFullNameReturnsFullName():
    testStudent = Student('1234', 'First', 'Last', 3.50)
    result = getFullName(testStudent)
    assert result == 'First Last'

testGetFullNameReturnsFullName()
