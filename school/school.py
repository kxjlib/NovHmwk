from people.sixth_form_student import SixthFormStudent
from people.student import Student
from people.teacher import Teacher
from people.enums.genderEnum import Gender

from typing import Union, Tuple

"""
School Class
Holds information about the school, and the people within.
"""


class School():
    school_ids_used = []

    def __init__(self, teachers: list = [], students: list = []):
        self.teachers = teachers
        self.students = students
        self.school_id = len(School.school_ids_used + 1)
        School.school_ids_used.append(self.school_id)

    """
    Add Teacher Method
    takes either a list of teachers or a singular teacher and adds it to the teachers list
    """

    def add_teacher(self, teacher: Union[list, Teacher]):
        if isinstance(teacher, Teacher):
            self.teachers += [teacher]
        elif isinstance(teacher, list):
            self.teachers += teacher
        else:
            raise ValueError("Teacher attribute neither a list or a Teacher")

    """
    Add Student Method
    takes either a list of students or a singular student and adds it to the students list
    """

    def add_student(self, student: Union[list, Student]):

        # This code will test what type the student property is
        # , and will either append just one student or all of them
        # We use isinstance because it will return true for
        # all 6th form students as well due to it testing parent classes
        if isinstance(student, Student):
            self.students += [student]
        elif isinstance(student, list):
            self.students += student
        else:
            raise ValueError("Student attribute neither a list or a Student")

    """
    Get Sixth Form Students Method
    From the self.students list, return all students that are 6th form students
    """

    def get_sixth_form_students(self) -> list:
        return [_ for _ in self.students if isinstance(_, SixthFormStudent)]

    """
    Get All Subject Learners
    Returns a tuple of all Teachers & Sixth Form Students that take a certain subject
    """

    def get_all_subject_learners(self, subject_name: str) -> Tuple[Teacher, SixthFormStudent]:
        # We use a list comprehension to return a subsection of the list in one line
        return ([_ for _ in self.teachers if subject_name in _.subjects_taught],
                [_ for _ in self.get_sixth_form_students() if subject_name in _.subjects])
