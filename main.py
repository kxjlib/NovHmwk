"""
William Davies
Python OOP Assessed Exercise
6.12.21
"""

from os import path
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

from school.school import School
from people.teacher import Teacher
from people.student import Student
from people.enums.genderEnum import Gender
from people.sixth_form_student import SixthFormStudent
from people.person import Person

def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
