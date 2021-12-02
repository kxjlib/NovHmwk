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

        self.create_menubar()

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
    def file_open_school(self, e=None):
        filename = askopenfilename(filetypes=(("Binary Files", "*.bin;*.dat"),
                                              ("All Files", "*.*")))
        # If the user did not choose a file
        if not filename:
            return

    # New School File Function
    def file_new_school(self, e=None):
        pass                            
