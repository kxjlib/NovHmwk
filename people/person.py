from people.genderEnum import Gender

"""
Person Parent Class
Holds information about name, age and gender of a person.
"""
class Person:
    def __init__(self, name:str, age:int, gender:Gender):
        self.name = name
        self.age = age
        self.gender = Gender