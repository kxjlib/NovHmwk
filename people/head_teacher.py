from people.teacher import Teacher

"""
Head Teacher Class
this is a subclass of teacher and also has the information regarding 
"""
class HeadTeacher(Teacher):
    def __init__(self, name: str, age: int, gender: str, school_identifier: int, salary: int, governor_names: list):
        super().__init__(name, age, gender, school_identifier, salary, [])
        self.governor_names = governor_names