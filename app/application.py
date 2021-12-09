import tkinter as tk
import tkcalendar
from tkinter.font import nametofont
from tkinter.filedialog import askopenfilename
from types import new_class

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
        self.new_person_button = tk.Button(self.ui_frame, text="Append Person", command=self.new_person)
        self.new_person_button.pack(side=tk.RIGHT,padx=40)


        # Remove Person Button
        self.new_person_button = tk.Button(self.ui_frame, text="Remove Person", command=self.remove_person)
        self.new_person_button.pack(side=tk.RIGHT)

        # Packs the "Canvas"
        self.ui_frame.pack(side=tk.LEFT)
    
    # This UI will be able to modify each individual person.
    def create_person_ui(self):
        # Create the frame that this UI will be rendered in
        self.person_frame = tk.Frame(self.root)

        # Name Entry
        self.name_entry = tk.Entry(self.person_frame,font=("TkDefaultFont 16"), justify='center')
        self.name_entry.insert(tk.END, "Full Name")
        self.name_entry.pack(pady=30)

        # Pack the UI
        self.person_frame.pack_propagate(0)
        self.person_frame.config(width=500)

        self.person_frame.pack(side=tk.RIGHT,fill=tk.BOTH)
        

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
            self.people_listbox.insert(tk.END, type_prefix[type(student)] + student.name)
    
    # New Person method.
    def new_person(self):
        pass

    # Remove Person method.
    def remove_person(self):
        pass
