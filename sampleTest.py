from sampleCode import Student, getFullName

def testGetFullNameReturnsFullName():
    testStudent = Student('1234', 14, 'Last', 3.50)
    result = getFullName(testStudent)
    assert result == 'First Last'

testGetFullNameReturnsFullName()
