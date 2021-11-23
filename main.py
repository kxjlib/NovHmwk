from people import sixth_form_student
from people import student
from people.teacher import Teacher
from school.school import School
"""
William Davies
Python OOP Assessed Exercise
6.12.21
"""

from people.student import Student
from people.enums.genderEnum import Gender
from people.sixth_form_student import SixthFormStudent
from people.person import Person


def main():
    wbs = School()

    bob_fishcake = Teacher("Bob Fishcake", 43, Gender.MALE,
                           43500, ["Economics", "Business"])

    wbs.add_teacher(bob_fishcake)

    thomas = SixthFormStudent("Tom Jaysinghe", 16, Gender.MALE, "The West Bridgford School", [
                              "Computer Science", "Physics", "Maths"])
    william = SixthFormStudent("Will Davies", 16, Gender.MALE, "The West Bridgford School", [
                              "Computer Science", "Economics", "Maths"])

    wbs.add_student([thomas, william])

    sixth_form_students = wbs.get_sixth_form_students()
    str_comp = ", \n".join([_.name for _ in sixth_form_students])
    str_sixth_form_students = f'Sixth Form Students ({len(sixth_form_students)}):\n{str_comp}'
    print(str_sixth_form_students)

    # TODO: Get All Teachers

    teachers_econ, students_econ = wbs.get_all_subject_learners("Economics")

    print(f"({len(teachers_econ)})({len(students_econ)})")

if __name__ == "__main__":
    main()
