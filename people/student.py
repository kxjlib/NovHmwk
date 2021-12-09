from people.person import Person
from people.enums.genderEnum import Gender

"""
Student Child Class
Holds extra information about school name.
"""


class Student(Person):
    def __init__(self, name: str, age: int, gender: Gender, school_identifier: int):
        super().__init__(name, age, gender, school_identifier)
