from people.student import Student
from people.genderEnum import Gender

"""
Sixth Form Student Child Class
Holds a subject list
"""
class SixthFormStudent(Student):
    def __init__(self, name: str, age: int, gender: Gender, school_name: str, subjects:list):
        super().__init__(name, age, gender, school_name)
        self.subjects = subjects