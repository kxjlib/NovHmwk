from people.person import Person

"""
Teacher Child Class
Holds extra information about salary and subjects taught.
"""


class Teacher(Person):
    def __init__(self, name: str, age: int, gender: str, school_identifier: int, salary: int, subjects: list):
        super().__init__(name, age, gender, school_identifier)
        self.salary = salary
        self.subjects = subjects
