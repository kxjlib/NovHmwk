"""
Person Parent Class
Holds information about name, age and gender of a person.
"""


class Person:
    def __init__(self, name: str, age: int, gender: str, school_identifier: int):
        self.name = name
        self.age = age
        self.gender = gender
