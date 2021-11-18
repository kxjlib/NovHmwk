from people.person import Person
from people.enums.genderEnum import Gender

"""
Teacher Child Class
Holds extra information about salary and subjects taught.
"""


class Teacher(Person):
    def __init__(self, name: str, age: int, gender: Gender, salary: int, subjects_taught: list):
        super().__init__(name, age, gender)
        self.salary = salary
        self.subjects_taught = subjects_taught
