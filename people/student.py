from people.person import Person
from people.genderEnum import Gender

"""
Student Child Class
Holds extra information about school name.
"""
class Student(Person):
    def __init__(self, name:str, age:int, gender:Gender, school_name: str):
        super().__init__(name, age, gender)
        self.school_name = school_name