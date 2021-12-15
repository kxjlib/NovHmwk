import tkinter as tk
import tkcalendar
from tkinter.font import nametofont
from tkinter.filedialog import askopenfilename, asksaveasfilename
from people.head_teacher import HeadTeacher

from people.sixth_form_student import SixthFormStudent
from people.student import Student
from people.teacher import Teacher

from school.school import School

import pickle

"""
Application Class
Holds information about the application window
and bundles in all methods relating to the GUI application
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
        file_menu.add_command(label="Save School File",accelerator="Ctrl+S")

        self.bind_fm_accelerators(file_menu)

        menubar.add_cascade(label="File", menu=file_menu, underline=0)

        self.root.config(menu=menubar)

    # Bind File Menu Accelerators Function:
    # Using the file_menu_shortcuts dict, bind all keyboard shortcuts related to the File menu

    def bind_fm_accelerators(self, file_menu):
        file_menu_shortcuts = {
            "<Control-o>": self.file_open_school,
            "<Control-n>": self.file_new_school,
            "<Control-s>": self.file_save_school
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
        self.people_listbox.bind('<<ListboxSelect>>', self.listbox_on_select)
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
        self.person_type = tk.OptionMenu(self.person_frame, self.person_type_var, "Head Teacher" ,"Teacher",
                                         "Student", "Sixth Form Student", command=self.type_specific_ui)
        self.person_type.place(relx=0.25, rely=0.45, anchor=tk.CENTER)

        """
        Teacher Specific UI
        """
        # Salary
        self.teacher_salary_var = tk.StringVar(self.person_frame)
        self.teacher_salary_label = tk.Label(
            self.person_frame, text="Salary", font=bold_font)
        # This line makes sure that only numbers can be inputted
        valcmd = (self.root.register(self.validate), '%d',
                  '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.teacher_salary_entry = tk.Entry(
            self.person_frame, textvariable=self.teacher_salary_var, validate='key', validatecommand=valcmd)

        # Subjects Taught
        self.subjects_taught_var = tk.StringVar(self.person_frame)
        self.subjects_taught_label = tk.Label(
            self.person_frame, text="Subjects", font=bold_font)
        self.subjects_taught_listbox = tk.Listbox(self.person_frame, height=8)
        self.subjects_taught_entry = tk.Entry(
            self.person_frame, textvariable=self.subjects_taught_var)
        self.subjects_taught_add = tk.Button(
            self.person_frame, text="Add", command=self.lessons_add)
        self.subjects_taught_del = tk.Button(
            self.person_frame, text="Del", command=self.lessons_del)

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
        self.yeargroup_label = tk.Label(
            self.person_frame, text="Year Group", font=bold_font)

        self.yeargroup_year_var = tk.StringVar(self.person_frame)
        self.yeargroup_year = tk.OptionMenu(
            self.person_frame, self.yeargroup_year_var, *"789", "10", "11", "12", "13")

        self.yeargroup_form_var = tk.StringVar(self.person_frame)
        self.yeargroup_form = tk.OptionMenu(
            self.person_frame, self.yeargroup_form_var, *"ABCDEFGHJ")

        """
        Head Teacher Specific UI
        """
        
        # Governor Names
        self.govn_names_var = tk.StringVar(self.person_frame)
        self.govn_names_label = tk.Label(
            self.person_frame, text="Governors", font=bold_font)
        self.govn_names_listbox = tk.Listbox(self.person_frame, height=8)
        self.govn_names_entry = tk.Entry(
            self.person_frame, textvariable=self.govn_names_var)
        self.govn_names_add = tk.Button(
            self.person_frame, text="Add", command=self.governor_add)
        self.govn_names_del = tk.Button(
            self.person_frame, text="Del", command=self.governor_del)

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
            # This try_except statement will catch any errors that may occur when opening the File
            # Such as EOF error (If you pass in an empty file)
            try:
                temp_school = pickle.load(file)
                self.school = temp_school
            except:
                print("[Error]: An Error occured when opening the file.")

        self.init_listbox()

    # New School File Function
    def file_new_school(self, _=None):
        self.school = School()
        self.init_listbox()
    
    def file_save_school(self, _=None):
        filename = asksaveasfilename(filetypes=(("Binary Files", "*.bin;*.dat"),("All Files","*.*")))

        if not filename:
            return

        with open(filename, 'wb') as file:
            pickle.dump(self.school, file)

    # Init listbox - Load all students and teachers into the listbox
    def init_listbox(self):
        type_prefix = {
            SixthFormStudent: '[SF] ',
            Student: '[LS] ',
            Teacher: '[TE] ',
            HeadTeacher: '[HT] ',
        }
        # Clear the listbox and reinsert all elements
        self.people_listbox.delete(0, tk.END)
        for person in self.school.people:
            self.people_listbox.insert(
                tk.END, type_prefix[type(person)] + person.name)

    # New Person method.
    def create_person(self):
        # Universal Information (Every Person Type has it)
        p_name = self.name_entry.get()
        p_dob = self.dob_calendar.get_date()
        p_gender = self.gender_var.get()

        p_type = self.person_type_var.get()

        # Student Specific Information
        if p_type == "Student":
            p_behaviour = self.behaviour_var.get()
            p_yeargroup = self.yeargroup_year_var.get() + self.yeargroup_form_var.get()
            p = Student(p_name, p_dob, p_gender,
                        self.school.school_id, p_yeargroup, p_behaviour)

        # Teacher Specific Information
        if p_type == "Teacher":
            p_salary = self.teacher_salary_var.get()
            if not p_salary:
                p_salary = 0
            p_salary = int(p_salary)
            p_subjects = list(self.subjects_taught_listbox.get(0, tk.END))
            p = Teacher(p_name, p_dob, p_gender,
                        self.school.school_id, p_salary, p_subjects)

        # Sixth Form Student Specific Information
        if p_type == "Sixth Form Student":
            p_subjects = list(self.subjects_taught_listbox.get(0, tk.END))
            p_behaviour = self.behaviour_var.get()
            p_yeargroup = self.yeargroup_year_var.get() + self.yeargroup_form_var.get()
            p = SixthFormStudent(
                p_name, p_dob, p_gender, self.school.school_id, p_yeargroup, p_behaviour, p_subjects)
        
        if p_type == "Head Teacher":
            p_salary = self.teacher_salary_var.get()
            if not p_salary:
                p_salary = 0
            p_salary = int(p_salary)
            p_governors = list(self.govn_names_listbox.get(0, tk.END))
            p = HeadTeacher(p_name,p_dob,p_gender,self.school.school_id,p_salary,p_governors)

        return p

    def new_person(self):
        p = self.create_person()
        all_people = [_.name for _ in self.school.people]
        p_name = p.name
        # Ensure that there is not a student of the same name
        if p_name not in all_people and p_name != "Name in use!":
            self.school.people.append(p)
            self.init_listbox()
        # Else set the name field to become an error
        else:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, "Name in use!")

    # Remove Person method.

    def remove_person(self):
        # Take Current Selection from people listbox and remove them from the school
        selected_person = self.people_listbox.curselection()
        if selected_person:
            p_del_name = self.people_listbox.get(selected_person[0])[5:]
            for i in range(0, len(self.school.people)):
                if self.school.people[i].name == p_del_name:
                    del self.school.people[i]
                    break

            self.init_listbox()

    # This method will take the person currently selected and replace them
    def edit_person(self):
        p = self.create_person()
        selected_person = self.people_listbox.curselection()
        if selected_person:
            # We find the name of the person we want to change as there may be
            # a situation where the list is not in the same order as the GUI
            p_edit_name = self.people_listbox.get(selected_person[0])[5:]
            for i in range(0, len(self.school.people)):
                if self.school.people[i].name == p_edit_name:
                    self.school.people[i] = p
                    break

        self.init_listbox()

    # This method will be called every time a person is selected

    def listbox_on_select(self, evt):
        p_types = {Student: "Student",
                   SixthFormStudent: "Sixth Form Student", Teacher: "Teacher", HeadTeacher: "Head Teacher"}

        selected_person = self.people_listbox.curselection()
        if not selected_person:
            return
        else:
            selected_person = selected_person[0]
        p_name = self.people_listbox.get(selected_person)[5:]
        # Find the person selected
        for i in range(0, len(self.school.people)):
            if self.school.people[i].name == p_name:
                p = self.school.people[i]
                break

        p_age = p.age
        p_gender = p.gender

        self.person_type_var.set(p_types[type(p)])
        self.type_specific_ui()

        # set Universal information into entries
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, p_name)

        self.dob_calendar.set_date = p_age

        self.gender_var.set(p_gender)

        # If p is Student or SixthFormStudent
        if isinstance(p, Student):
            # Get Year Group and Behaviour
            if len(p.yeargroup) == 3:
                p_year = p.yeargroup[0:1]
                p_form = p.yeargroup[-1]
            elif len(p.yeargroup) == 2:
                p_year = p.yeargroup[0]
                p_form = p.yeargroup[-1]
            else:
                p_year = ""
                p_form = ""

            p_behaviour = p.behaviour

            # Set Student Specific Information
            self.behaviour_var.set(p_behaviour)
            self.yeargroup_form_var.set(p_form)
            self.yeargroup_year_var.set(p_year)

        # Sixth Form Student & Teacher Specific Information
        if isinstance(p, SixthFormStudent) or isinstance(p, Teacher):
            p_subjects = p.subjects

            self.subjects_taught_listbox.delete(0, tk.END)
            self.subjects_taught_listbox.insert(tk.END, *p_subjects)

        # Teacher and Head Teacher specific Information
        if isinstance(p, Teacher):
            p_salary = str(p.salary)
            self.teacher_salary_entry.delete(0, tk.END)
            self.teacher_salary_var.set(p_salary)
        
        # Head Teacher Specific Information
        if isinstance(p,HeadTeacher):
            p_governors = p.governor_names
            self.govn_names_listbox.delete(0, tk.END)
            self.govn_names_listbox.insert(tk.END, *p_governors)

    # Lessons add Method
    # Adds a Lesson from the subjects entrybox into subjects_taught listbox
    def lessons_add(self):
        lesson = self.subjects_taught_entry.get()
        if lesson.lower() not in [_.lower() for _ in self.subjects_taught_listbox.get(0, tk.END)]:
            self.subjects_taught_listbox.insert(tk.END, lesson)

    # Removes lesson from subjects taught listbox based on which one was selected
    def lessons_del(self):
        lesson = self.subjects_taught_listbox.curselection()[0]
        self.subjects_taught_listbox.delete(lesson)

    # Add Governor to Governors Listbox
    def governor_add(self):
        governor = self.govn_names_entry.get()
        if governor.lower() not in [_.lower() for _ in self.govn_names_listbox.get(0, tk.END)]:
            self.govn_names_listbox.insert(tk.END, governor)

    # Remove Governors from Listbox
    def governor_del(self):
        governor = self.govn_names_listbox.curselection()[0]
        self.govn_names_listbox.delete(governor)

    # Binds the Subject Box
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
            self.yeargroup_label,
            self.govn_names_add,
            self.govn_names_del,
            self.govn_names_entry,
            self.govn_names_label,
            self.govn_names_listbox,
        ]

        for widget in widgets_to_unbind:
            widget.place_forget()

        self.teacher_salary_var.set("")
        self.subjects_taught_listbox.delete(0, tk.END)
        self.subjects_taught_var.set("")
        self.govn_names_listbox.delete(0,tk.END)
        self.govn_names_var.set("")

        # Teacher Specific UI
        if self.person_type_var.get() == "Teacher":
            self.teacher_salary_label.place(
                relx=0.75, rely=0.4, anchor=tk.CENTER)
            self.teacher_salary_entry.place(
                relx=0.75, rely=0.45, anchor=tk.CENTER)
            self.bind_subjects_box()
        
        # Head Teacher Specific UI
        elif self.person_type_var.get() == "Head Teacher":
            self.teacher_salary_label.place(
                relx=0.75, rely=0.4, anchor=tk.CENTER)
            self.teacher_salary_entry.place(
                relx=0.75, rely=0.45, anchor=tk.CENTER)

            self.govn_names_label.place(
            relx=0.75, rely=0.55, anchor=tk.CENTER)
            self.govn_names_listbox.place(
                relx=0.75, rely=0.7, anchor=tk.CENTER)
            self.govn_names_entry.place(
                relx=0.75, rely=0.85, anchor=tk.CENTER)
            self.govn_names_add.place(relx=0.8, rely=0.9, anchor=tk.CENTER)
            self.govn_names_del.place(relx=0.7, rely=0.9, anchor=tk.CENTER)

        # Student Specific UI
        elif self.person_type_var.get() == "Student":
            self.behaviour.place(relx=0.25, rely=0.6, anchor=tk.CENTER)
            self.behaviour_label.place(relx=0.25, rely=0.55, anchor=tk.CENTER)
            self.yeargroup_form.place(relx=0.3, rely=0.75, anchor=tk.CENTER)
            self.yeargroup_year.place(relx=0.2, rely=0.75, anchor=tk.CENTER)
            self.yeargroup_label.place(relx=0.25, rely=0.7, anchor=tk.CENTER)

        # Sixth Form Student Specific UI
        elif self.person_type_var.get() == "Sixth Form Student":
            self.behaviour.place(relx=0.25, rely=0.6, anchor=tk.CENTER)
            self.behaviour_label.place(relx=0.25, rely=0.55, anchor=tk.CENTER)
            self.yeargroup_form.place(relx=0.3, rely=0.75, anchor=tk.CENTER)
            self.yeargroup_year.place(relx=0.2, rely=0.75, anchor=tk.CENTER)
            self.yeargroup_label.place(relx=0.25, rely=0.7, anchor=tk.CENTER)
            self.bind_subjects_box()

    # Validate Method - Makes sure a field is exclusively numbers
    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        if(action == '1'):
            if text in '0123456789':
                return True
            return False
        return True
