from people.student import Student

"""
Sixth Form Student Child Class
Holds a subject list
"""


class SixthFormStudent(Student):
    def __init__(self, name: str, age: int, gender: str, school_identifier: int,  yeargroup:str, behaviour:str, subjects: list):
        super().__init__(name, age, gender, school_identifier, yeargroup, behaviour)
        self.subjects = subjects
