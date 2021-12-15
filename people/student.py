from people.person import Person

"""
Student Child Class
Holds extra information about school name.
"""


class Student(Person):
    def __init__(self, name: str, age: int, gender: str, school_identifier: int, yeargroup:str, behaviour: str):
        super().__init__(name, age, gender, school_identifier)
        self.yeargroup = yeargroup
        self.behaviour = behaviour
