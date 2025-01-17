import os, json, tempfile
import tkinter as tk
from copy import deepcopy
from validator import validate_unique, validate_chars
import save_handler as saves

class HallManager():
    '''
    This class provides a tk.Toplevel widget allowing users to
    modify the key phrases used to identify the applicant's
    assigned dining hall, as well as the folder names to
    sort the given files into.
    '''
    def __init__(self, master):
        '''
        Parameters:
            - master: Organizer
                The main Organizer containing the folder
                selection window and the hall settings.
        '''
        self.master = master
        self.window = tk.Toplevel(master.window)
        self.window.grab_set()
        self.window.title("Dining Hall Settings")
        self.window.resizable(False, False)
        self.halls = saves.get_saves()
        self.modified_version = deepcopy(self.halls)
        self.new_hall_adder = NewHallAdder(self)
        self.curr_hall_table = HallTable(self)

    def start(self):
        '''
        This function mainloops the Tk in this object.
        When mainloop ends (aka the Tk is closed), the
        dictionary of halls is returned.
        '''
        self.window.mainloop()

class NewHallAdder():
    '''
    This class provides a tk.Frame to allow users to add
    new dining halls (dining hall name, key phrase, and 
    folder name) to the HallNameSetter.
    '''
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master.window, bd=7, relief="ridge")
        self.frame.grid(row=0, column=0)

        self.title = tk.Label(self.frame, text="Add a New Hall!", bd=5, relief="groove", padx=5, pady=5, bg='lightblue', width=55)
        self.title.grid(row=0, column=0, columnspan=3, sticky="we")

        self.name_label = tk.Label(self.frame, text="Dining Hall Name")
        self.name_label.grid(row=1, column=0)
        self.name_entry = tk.Entry(self.frame, bg='white', bd=5)
        self.name_entry.grid(row=2, column=0)

        self.key_label = tk.Label(self.frame, text="Key Phrase")
        self.key_label.grid(row=1, column=1)
        self.key_entry = tk.Entry(self.frame, bg='white', bd=5)
        self.key_entry.grid(row=2, column=1)

        self.dir_label = tk.Label(self.frame, text="Folder Name")
        self.dir_label.grid(row=1, column=2)
        self.dir_entry = tk.Entry(self.frame, bg='white', bd=5)
        self.dir_entry.grid(row=2, column=2)

        self.result_label = tk.Label(self.frame)
        self.result_label.grid(row=3, column=0, columnspan=2, sticky='we')

        self.submit_button = tk.Button(self.frame, text="Add", bg='white', padx=4, pady=2, command=self.submit)
        self.submit_button.grid(row=3, column=2, sticky="we")
        
    def submit(self):
        '''
        The action taken when the submit button is clicked.
        
        Checks the following errors in the order listed:
        1. The new dining hall name is empty.
        2. The new dining hall name is not unique.
        3. The new key phrase is empty.
        4. The new key phrase contains illegal chars for file names.
        5. The new key phrase is already in use by another hall.
        6. The new folder name is empty.
        7. The new folder name contains illegal chars for folder paths.
        8. The new folder name is already in use by another hall.

        If no errors are found, pass the new entry back to the parent
        HallNameSetter and clear out the entries for the next hall.
        '''
        curr_names = []
        curr_keys = []
        curr_dirnames = []
        for hall_name, keypair in self.master.modified_version.items():
            curr_names.append(hall_name)
            curr_keys.append(keypair[0])
            curr_dirnames.append(keypair[1])
        
        new_name = self.name_entry.get().strip()
        new_key = self.key_entry.get().strip()
        new_dirname = self.dir_entry.get().strip()
        if not new_name:
            self.result_label.config(text="Name cannot be empty!", bg='red')
            return
        if not validate_unique(new_name, curr_names):
            self.result_label.config(text="Name is already used!", bg='red')
            return
        if not new_key:
            self.result_label.config(text="Key Phrase cannot be empty!", bg='red')
            return
        if not validate_chars(new_key):
            self.result_label.config(text="Key Phrase contains illegal characters!", bg='red')
            return
        if not validate_unique(new_key, curr_keys):
            self.result_label.config(text="Key Phrase is already used!", bg='red')
            return
        if not new_dirname:
            self.result_label.config(text="Folder Name cannot be empty!", bg='red')
            return
        if not validate_chars(new_dirname):
            self.result_label.config(text="Folder Name contains illegal characters!", bg='red')
            return
        if not validate_unique(new_dirname, curr_dirnames):
            self.result_label.config(text="Folder Name is already used!", bg='red')
            return
        
        self.master.modified_version[new_name] = [new_key, new_dirname]
        self.name_entry.delete(0, len(self.name_entry.get()))
        self.key_entry.delete(0, len(self.key_entry.get()))
        self.dir_entry.delete(0, len(self.dir_entry.get()))
        self.result_label.config(text=f"{new_name} has been added to your Halls!", bg='lightgreen')
        self.master.curr_hall_table.render_new(new_name, [new_key, new_dirname])
        self.name_entry.focus_set()

class HallTable():
    '''
    This class provides a Tk.Frame to allow users to
    see their current dining hall settings, including
    the dining hall name, key phrase, and folder name.
    
    This also provides the ability to modify and delete
    the existing halls, provided that uniqueness and 
    validity of the key phrases and folder names are 
    satisfied and preserved.
    '''
    def __init__(self, master):
        '''
        Parameters:
            - master: HallManager
                The parent HallManager object containing the
                Tk that this HallTable's frame is placed in.
        '''
        self.master = master
        self.frame = tk.Frame(master.window, bd=7, relief="ridge")
        self.frame.grid(row=1, column=0, sticky="we")

        self.title = tk.Label(self.frame, text="Current Halls", bd=5, relief="groove", padx=5, pady=5, bg='lightblue', width=55)
        self.title.grid(row=0, column=0, sticky="ew")

        self.rows = []
        self.empty_msg = tk.Label(self.frame, text="You don't have any halls! Add more above!", bg='white', padx=5, bd=5)
        self.save_bar = tk.Frame(self.frame)
        self.save_result = tk.Label(self.save_bar, width=50)
        self.save_result.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.save_button = tk.Button(self.save_bar, text="Save", width=6, command=self.save)
        self.save_button.grid(row=0, column=2, sticky="ew")
        self.render_start()
    
    def render_empty(self):
        '''
        This function renders the empty message and the
        save bar. Requires the precondition that there
        are no rows present in the table (i.e. self.rows
        is empty).
        '''
        self.save_bar.grid_forget()
        self.empty_msg.grid(row=1, column=0, sticky="ew")
        self.render_save("", self.master.window.cget("background"))
        self.save_bar.grid(row=2, column=0, sticky="ew")

    def render_new(self, new_hall, new_keypair):
        '''
        This function adds a new entry into the table.
        If the table is originally empty, this function
        first removes the empty message label before
        rendering.

        Parameters:
            - new_hall: str
                The name of the new hall to be added and rendered.
            - new_keypair: List[str]
                The 2-length array containing the key phrase and
                folder name for the new hall.
        '''
        self.render_save("", self.master.window.cget("background"))
        self.save_bar.grid_forget()
        row_num = len(self.rows) + 1
        if row_num == 1:
            self.empty_msg.grid_forget()
        self.rows.append(HallRow(self, new_hall, new_keypair, row_num, 0))
        self.save_bar.grid(row=row_num+1, column=0, sticky="ew")

    def render_start(self):
        '''
        This function is only to be used when rendering the
        frame and all rows for the first time.
        '''
        if len(self.master.halls) == 0:
            self.render_empty()
        else:
            row_num = 1
            for hall_name, keypair in self.master.halls.items():
                self.rows.append(HallRow(self, hall_name, keypair, row_num, 0))
                row_num += 1
            self.save_bar.grid(row=row_num, column=0, sticky="ew")

    def render_save(self, save_msg, save_color):
        '''
        This function updates the save message used to
        display the results of any new or save actions.
        '''
        self.save_result.config(text=save_msg, bg=save_color)

    def save(self):
        '''
        This function attempts to save the user's choices
        into the main dictionary. Fails in the following cases,
        listed by priority of checking:

        1. An empty key phrase is found.
        2. An invalid character is found in the key phrase.
        3. An empty folder name is found.
        4. An invalid character is found in the folder name.
        5. A duplicate is found, either between the key phrases
           or between the folder names. This can stack all.

        The main dictionary is updated if no entries exist, or 
        all checks are successful.
        '''
        if len(self.rows) == 0:
            self.master.halls = dict()
            self.master.modified_version = dict()
            self.render_save("Saved!", "lightgreen")
            return
        for row in self.rows:
            row.key.config(bg='white')
            row.dir.config(bg='white')
        error_found = False
        result_str = ""
        new_names = []
        new_keys = []
        new_dirs = []
        for row in self.rows:
            new_names.append(row.hall_entry)
            new_key = row.key.get().strip()
            new_dir = row.dir.get().strip()
            if len(new_key) == 0:
                self.render_save("Key Phrase cannot be empty!", 'red')
                row.key.config(bg='red')
                return
            if not validate_chars(new_key):
                self.render_save("Key Phrase cannot contain illegal characters!", 'red')
                row.key.config(bg='red')
                return
            new_keys.append(new_key)
            if len(new_dir) == 0:
                self.render_save("Folder Name cannot be empty!", 'red')
                row.dir.config(bg='red')
                return
            if not validate_chars(new_dir):
                self.render_save("Folder Name cannot contain illegal characters!", 'red')
                row.dir.config(bg='red')
                return
            new_dirs.append(new_dir)
        key_dupes = dict()
        dir_dupes = dict()
        for idx in range(len(new_names)):
            if new_keys[idx] in key_dupes:
                self.rows[key_dupes[new_keys[idx]][-1]].key.config(bg='red')
                self.rows[idx].key.config(bg='red')
                key_dupes[new_keys[idx]].append(idx)
                error_found = True
            else:
                key_dupes[new_keys[idx]] = [idx]
            if new_dirs[idx] in dir_dupes:
                self.rows[dir_dupes[new_dirs[idx]][-1]].dir.config(bg='red')
                self.rows[idx].dir.config(bg='red')
                dir_dupes[new_dirs[idx]].append(idx)
                error_found = True
            else:
                dir_dupes[new_dirs[idx]] = [idx]
        if error_found:
            self.render_save("Key Phrases and Folder Names must be unique!", 'red')
        else:
            self.master.halls = dict()
            for idx in range(len(new_names)):
                self.master.halls[new_names[idx]] = [new_keys[idx].strip(), new_dirs[idx].strip()]
            self.master.modified_version = deepcopy(self.master.halls)
            saves.post_saves(self.master.halls)
            self.render_save("Saved!", 'lightgreen')

class HallRow():
    '''
    This class provides individual rows for the HallTable.
    Each row displays a Dining Hall Name, Key Phrase, 
    Folder Name, as well as a button to delete itself from
    the table.
    '''
    def __init__(self, master, row_name, row_keypair, row, column):
        '''
        Parameters:
            - master: HallTable
                The parent HallTable object that the row is being
                inserted into.
            - row_name: str
                The main name of the dining hall to be displayed
            - row_keypair: List[str]
                The 2-length array containing [key phrase, dirname]
            - row: int
                The index of the row in the master HallTable's frame
                where this HallRow's frame should be placed
            - column: int
                The index of the column in the master HallTable's
                frame where this HallRow's frame should be placed
        '''
        self.master = master
        self.hall_entry = row_name
        self.location = row - 1
        self.frame = tk.Frame(master.frame, width=55)
        self.name = tk.Label(self.frame, text=row_name, width=16, anchor="w")
        self.name.grid(row=0, column=0)
        self.key = tk.Entry(self.frame, bd=5)
        self.key.insert(0, row_keypair[0])
        self.key.grid(row=0, column=1)
        self.dir = tk.Entry(self.frame, bd=5)
        self.dir.insert(0, row_keypair[1])
        self.dir.grid(row=0, column=2)
        self.del_button = tk.Button(self.frame, text="x", command=self.del_row, width=2)
        self.del_button.grid(row=0, column=3)
        self.frame.grid(row=row, column=column)

    def del_row(self):
        '''
        This function deletes the displayed entry from the main
        dictionary, destroys the frame, and removes itself from
        the parent frame, updating all subsequent indices.
        '''
        self.master.master.modified_version.pop(self.hall_entry)
        self.master.rows.pop(self.location)
        for idx in range(self.location, len(self.master.rows)):
            self.master.rows[idx].location -= 1
        self.frame.destroy()
        if len(self.master.rows) == 0:
            self.master.render_empty()

    def grid(self, row, column):
        '''
        This helper function places the row into the master's
        frame.
        '''
        self.frame.grid(row=row, column=column, sticky="ew")

if __name__ == "__main__":
    new_window = HallNameSetter(dict())
    print(new_window.start())