import tkinter as tk
import tkcalendar
from tkinter.font import nametofont
from tkinter.filedialog import askopenfilename

import datetime

from people.sixth_form_student import SixthFormStudent
from people.student import Student
from people.teacher import Teacher

from school.school import School

import pickle

"""
Application Class
Holds information about the application window
and bundles in all methods relating to the application
"""


class Application:
    def __init__(self):
        # Initialise Window and set settings
        self.root = tk.Tk()
        self.root.geometry('800x600')
        self.root.resizable(False, False)
        self.root.title("School Management System")
        self.root.iconbitmap("assets/window_icon.ico")
        # Set Default Font
        default_font = nametofont("TkDefaultFont")
        default_font.configure(size=9)
        self.root.option_add("*Font", default_font)

        self.school = School()

        self.create_menubar()
        self.pack_ui()

    """
    Window Init & Run Methods
    """
    # Create Menubar Function:
    # Creates a menubar (File,edit etc) and stores it in the config of self.root

    def create_menubar(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open School File",
                              command=self.file_open_school,
                              accelerator="Ctrl+O")
        file_menu.add_command(label="Create New School File",
                              command=self.file_new_school,
                              accelerator="Ctrl+N")

        self.bind_fm_accelerators(file_menu)

        menubar.add_cascade(label="File", menu=file_menu, underline=0)

        self.root.config(menu=menubar)

    # Bind File Menu Accelerators Function:
    # Using the file_menu_shortcuts dict, bind all keyboard shortcuts related to the File menu

    def bind_fm_accelerators(self, file_menu):
        file_menu_shortcuts = {
            "<Control-o>": self.file_open_school,
            "<Control-n>": self.file_new_school
        }

        for binding, command in file_menu_shortcuts.items():
            file_menu.bind_all(binding, command)

    # Creates the UI as a whole
    def pack_ui(self):
        self.create_listbox_ui()
        self.create_person_ui()

    # This method creates the UI that appears on the left.
    def create_listbox_ui(self):
        # Here we are creating a frame which is being used to draw to.
        # A "canvas" which we draw to
        self.ui_frame = tk.Frame(self.root)
        self.listbox_scrollbar = tk.Scrollbar(
            self.ui_frame, orient=tk.VERTICAL)
        # This listbox holds all people of the school in
        self.people_listbox = tk.Listbox(
            self.ui_frame, width=50, height=30, yscrollcommand=self.listbox_scrollbar.set)

        # Configure Scrollbar
        self.listbox_scrollbar.config(command=self.people_listbox.yview)

        self.listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.people_listbox.pack(pady=15)

        # Create the New Person Button
        self.new_person_button = tk.Button(
            self.ui_frame, text="Add", command=self.new_person)
        self.new_person_button.pack(side=tk.RIGHT, padx=35)

        self.edit_person_button = tk.Button(
            self.ui_frame, text="Edit", command=self.edit_person)
        self.edit_person_button.pack(side=tk.RIGHT, padx=35)

        # Remove Person Button
        self.new_person_button = tk.Button(
            self.ui_frame, text="Del", command=self.remove_person)
        self.new_person_button.pack(side=tk.RIGHT, padx=35)

        # Packs the "Canvas"
        self.ui_frame.pack(side=tk.LEFT)

    # This UI will be able to modify each individual person.
    def create_person_ui(self):
        # Create the frame that this UI will be rendered in
        self.person_frame = tk.Frame(self.root)

        bold_font = ("TkDefault 12 bold")

        # Name Entry
        self.name_entry = tk.Entry(self.person_frame, font=(
            "TkDefaultFont 16"), justify='center', width=25)
        self.name_entry.insert(tk.END, "Full Name")
        self.name_entry.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        # DOB entry Label
        self.dob_label = tk.Label(
            self.person_frame, text="DOB", font=bold_font)
        self.dob_label.place(relx=0.25, rely=0.2, anchor=tk.CENTER)

        # DOB DatePicker
        self.dob_calendar = tkcalendar.DateEntry(self.person_frame, width=10)
        self.dob_calendar.place(relx=0.25, rely=0.25, anchor=tk.CENTER)

        # Gender entry Label
        self.gender_label = tk.Label(
            self.person_frame, text="Gender", font=bold_font)
        self.gender_label.place(relx=0.75, rely=0.2, anchor=tk.CENTER)

        # Gender Dropdown.
        self.gender_var = tk.StringVar(self.person_frame)
        self.gender_var.set("Male")
        self.gender_dropdown = tk.OptionMenu(
            self.person_frame, self.gender_var, "Male", "Female", "Other")
        self.gender_dropdown.place(relx=0.75, rely=0.25, anchor=tk.CENTER)

        # Person Type Label
        self.person_type_label = tk.Label(
            self.person_frame, text="Person Type", font=bold_font)
        self.person_type_label.place(relx=0.25, rely=0.4, anchor=tk.CENTER)

        # Person Type Dropdown.
        self.person_type_var = tk.StringVar(self.person_frame)
        self.person_type = tk.OptionMenu(self.person_frame, self.person_type_var, "Teacher",
                                         "Student", "Sixth Form Student", command=self.type_specific_ui)
        self.person_type.place(relx=0.25, rely=0.45, anchor=tk.CENTER)

        """
        Teacher Specific UI
        """
        # Salary
        self.teacher_salary_label = tk.Label(
            self.person_frame, text="Salary", font=bold_font)
        # This line makes sure that only numbers can be inputted
        valcmd = (self.root.register(self.validate), '%d',
                  '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.teacher_salary_entry = tk.Entry(
            self.person_frame, validate='key', validatecommand=valcmd)

        # Subjects Taught
        self.subjects_taught_label = tk.Label(
            self.person_frame, text="Subjects", font=bold_font)
        self.subjects_taught_listbox = tk.Listbox(self.person_frame, height=8)
        self.subjects_taught_entry = tk.Entry(self.person_frame)
        self.subjects_taught_add = tk.Button(
            self.person_frame, text="Add")
        self.subjects_taught_del = tk.Button(
            self.person_frame, text="Del")

        """
        Student Specific UI
        """

        self.behaviour_label = tk.Label(
            self.person_frame, text="Behaviour", font=bold_font)
        self.behaviour_var = tk.StringVar(self.person_frame)
        self.behaviour = tk.OptionMenu(
            self.person_frame, self.behaviour_var, "Good", "Average", "Bad")

        self.behaviour_var.set("Average")

        # Year Group
        self.yeargroup_label = tk.Label(self.person_frame, text="Year Group",font=bold_font)

        self.yeargroup_year_var = tk.StringVar(self.person_frame)
        self.yeargroup_year = tk.OptionMenu(self.person_frame, self.yeargroup_year_var, *"789","10","11","12","13")

        self.yeargroup_form_var = tk.StringVar(self.person_frame)
        self.yeargroup_form = tk.OptionMenu(self.person_frame, self.yeargroup_form_var, *"ABCDEFGHJ")


        # DEFAULT PERSON TYPE
        self.person_type_var.set("Student")
        self.type_specific_ui()

        # Pack the UI
        self.person_frame.config(width=500)
        self.person_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

    # Run function:
    # Runs the application by opening the window

    def run(self):
        self.root.mainloop()

    """
    Application methods
    """
    # Presents an open file prompt for the user to select a school file,
    # the e=None is there because for some reason tkinter passes an extra parameter
    # when you open a file using a keybinding.
    # _ argument does nothing but if removed then it doesn't work because of tkinter.

    def file_open_school(self, _=None):
        filename = askopenfilename(filetypes=(("Binary Files", "*.bin;*.dat"),
                                              ("All Files", "*.*")))
        # If the user did not choose a file
        if not filename:
            return

        with open(filename, 'rb') as file:
            self.school = pickle.load(file)

        self.init_listbox()

    # New School File Function
    def file_new_school(self, _=None):
        self.school = School()
        self.init_listbox()

    # Init listbox - Load all students and teachers into the listbox
    def init_listbox(self):
        type_prefix = {
            SixthFormStudent: '[SF] ',
            Student: '[LS] ',
            Teacher: '[TE] ',
        }
        self.people_listbox.delete(0, tk.END)
        for student in self.school.students:
            self.people_listbox.insert(
                tk.END, type_prefix[type(student)] + student.name)

    # New Person method.
    def new_person(self):
        p_name = self.name_entry.get()
        p_dob = self.dob_calendar.get_date()
        p_gender = self.gender_var.get()

        p_type = self.person_type_var.get()

        if p_type == "Student":
            p_behaviour = self.behaviour_var.get()
            p_yeargroup = self.yeargroup_year_var.get() + self.yeargroup_form_var.get()
            Student(p_name, p_dob, p_gender, self.school.school_id, p_yeargroup, p_behaviour)

    # Remove Person method.
    def remove_person(self):
        pass

    def edit_person(self):
        pass

    def bind_subjects_box(self):
        self.subjects_taught_label.place(
            relx=0.75, rely=0.55, anchor=tk.CENTER)
        self.subjects_taught_listbox.place(
            relx=0.75, rely=0.7, anchor=tk.CENTER)
        self.subjects_taught_entry.place(
            relx=0.75, rely=0.85, anchor=tk.CENTER)
        self.subjects_taught_add.place(relx=0.8, rely=0.9, anchor=tk.CENTER)
        self.subjects_taught_del.place(relx=0.7, rely=0.9, anchor=tk.CENTER)

    def type_specific_ui(self, _=None):
        # Unbind all Widgets
        widgets_to_unbind = [
            self.teacher_salary_entry,
            self.teacher_salary_label,
            self.subjects_taught_add,
            self.subjects_taught_del,
            self.subjects_taught_entry,
            self.subjects_taught_listbox,
            self.subjects_taught_label,
            self.behaviour,
            self.behaviour_label,
            self.yeargroup_year,
            self.yeargroup_form,
            self.yeargroup_label
        ]

        for widget in widgets_to_unbind:
            widget.place_forget()

        if self.person_type_var.get() == "Teacher":
            self.teacher_salary_label.place(
                relx=0.75, rely=0.4, anchor=tk.CENTER)
            self.teacher_salary_entry.place(
                relx=0.75, rely=0.45, anchor=tk.CENTER)
            self.bind_subjects_box()

        elif self.person_type_var.get() == "Student":
            self.behaviour.place(relx=0.25, rely=0.6, anchor=tk.CENTER)
            self.behaviour_label.place(relx=0.25, rely=0.55, anchor=tk.CENTER)
            self.yeargroup_form.place(relx=0.3,rely=0.75, anchor=tk.CENTER)
            self.yeargroup_year.place(relx=0.2,rely=0.75,anchor=tk.CENTER)
            self.yeargroup_label.place(relx=0.25, rely=0.7, anchor=tk.CENTER)

        elif self.person_type_var.get() == "Sixth Form Student":
            self.behaviour.place(relx=0.25, rely=0.6, anchor=tk.CENTER)
            self.behaviour_label.place(relx=0.25, rely=0.55, anchor=tk.CENTER)
            self.yeargroup_form.place(relx=0.3,rely=0.75, anchor=tk.CENTER)
            self.yeargroup_year.place(relx=0.2,rely=0.75,anchor=tk.CENTER)
            self.yeargroup_label.place(relx=0.25, rely=0.7, anchor=tk.CENTER)
            self.bind_subjects_box()

    # Validate Method - Makes sure a field is exclusively numbers
    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        if(action == '1'):
            if text in '0123456789':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True
