import os, json, tempfile
import re
import tkinter as tk
from tkinter.filedialog import askdirectory
from playwright.sync_api import sync_playwright
import playwright_funcs as pwfuncs
import pandas as pd
from datetime import datetime as dt
from HallManagerTk import HallManager
import save_handler as saves

class Organizer():
    '''
    This class provides a tk.Tk widget allowing users
    to select the input and output paths used to read
    files from and output files to.
    '''
    def __init__(self):
        self.source = None
        self.dest = None

        self.window = tk.Tk()
        self.window.title("File Organizer")
        self.window.resizable(False, False)

        self.frame = tk.Frame(self.window, bd=7, relief="ridge")
        self.frame.grid(row=0, column=0)

        self.all_folders = tk.BooleanVar()
        self.all_folders.set(False)

        self.log = tk.BooleanVar()
        self.log.set(True)

        self._get_menu()

        self.source_btn = self._get_button("Choose Input Folder", self.set_source, 0, 0)
        self.dest_btn = self._get_button("Choose Output Folder", self.set_dest, 1, 0)
        self.sort_btn = self._get_button("Sort", self.sort, 2, 0, fill=False)
        self.sort_btn.config(state=tk.DISABLED)

        self.source_entry = self._get_new_entry(0, 1)
        self.dest_entry = self._get_new_entry(1, 1)

        self.status = tk.Label(self.frame, text="No folders selected!", bg='red')
        self.status.grid(row=2, column=1)

    def _get_menu(self):
        '''
        This function creates and attaches 
        the main menubar.
        '''
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        self._get_settings_menu(menubar)
        self._get_info_menu(menubar)
    
    def _get_settings_menu(self, menubar):
        '''
        This function adds the Settings submenu to 
        the main menubar.

        Parameters:
            - menubar: tk.Menu
                The main menubar.
        '''
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Dining Hall Settings", command=self._open_hall_settings)
        settings_menu.add_separator()
        settings_menu.add_checkbutton(label="Create All Folders", onvalue=True, offvalue=False, variable=self.all_folders)
        settings_menu.add_checkbutton(label="Create Log File", onvalue=True, offvalue=False, variable=self.log)
        menubar.add_cascade(label="Settings", menu=settings_menu)

    def _open_hall_settings(self):
        '''
        This function opens a HallManager to allow the
        user to modify the settings in place for the halls.
        '''
        HallManager(self).start()
    
    def _get_info_menu(self, menubar):
        '''
        This function adds the Info menu to the
        main menubar.

        Parameters:
            - menubar: tk.Menu
                The main menubar.
        '''
        info_menu = tk.Menu(menubar, tearoff=0)
        info_menu.add_command(label="How to Use", command=self._open_how_to_use)
        info_menu.add_command(label="About", command=self._open_about)
        menubar.add_cascade(label="Info", menu=info_menu)

    def _open_how_to_use(self):
        '''
        This function opens an info box with the information
        regarding how to use this application.
        '''
        message = """
            Welcome to the Help page! Please ensure that you
            have an internet connection before using this app,
            as the app is unusable otherwise.

            To use this application, you must choose the input
            folder (where all of your DocuSign PDFs are located)
            and your output folder (where your files will go).
            Your DocuSign PDFs must be named in the format:

            (Name) (Survey Number) <(Dining Hall).pdf

            Ensure that you have spaces between the three
            components, as they are required in this version!

            You can change the key phrases used to identify the
            dining halls under the Settings menu, where you can
            select "Dining Hall Settings" to open a new window
            that will allow you to modify your settings.

            By default, only the necessary folders will be made,
            i.e. if there are no applicants for a dining hall,
            then the folder for that dining hall will not be
            created. You can also toggle this setting under the
            Settings menu by checking or unchecking the "Create
            All Folders" option.

            Logging is on by default. To change this, go under
            Settings and check or uncheck the "Create Log File"
            option. If logging is turned on, an excel sheet with
            the name "YYYY-MM-DD-HH-MM-SS.xlsx" will be created
            in your output folder. If no Scheduling Survey number
            was provided, "-1" will be placed in the log file.

            Happy Sorting!
        """
        tk.messagebox.showinfo(title="How to Use", message=message)

    def _open_about(self):
        '''
        This function opens an info box with the 
        About information.
        '''
        message = """
            Welcome to the Virginia Tech Dining Services Central
            Hiring Office Administrative File Organizer application.
            Or, you know... just call it the File Organizer...

            Version 2.0 of this application requires a network
            connection, but allows you to avoid having to go to
            the Microsoft Forms page and manually downloading 
            the Scheduling Survey PDFs.

            The same flaw from Version 1.0 still exists due to the
            limitations of the computer's file system, which is:

            * If two (or more) students have the same name and
              are going to the same dining hall, only the first
              person will be sorted. All other applicants will 
              appear as unsorted, and they will pop up under the 
              Duplicates page in the log file (provided you allow 
              logging). Avoid this issue by using a different name
              for the other applicants, or remove the original file
              from the sorting location.
            
            Version: 2.0
            Creator: 
                Kevin Chen
                VT Class of 2025
                Senior Student Hiring Administrator (SHA)
                BS Computer Science and BS Math
        """
        tk.messagebox.showinfo(title="About", message=message)

    def _get_button(self, label, onclick, row, column, fill=True):
        '''
        This function creates a button with the label as
        text, and the onclick function as the callback function.
        After generation, it will add the button to the main
        frame at the row and column indices.

        Parameters:
            - label: str
                The text to place on the button.
            - onclick: function
                The callback function linked to the button.
            - row: int
                The row index in the frame it will be placed in.
            - column: int
                The column index in the frame it will be placed in.
            - fill: bool
                If True, the button will have sticky set to 'ew'.
        '''
        btn = tk.Button(self.frame, text=label, bg='white', command=onclick)
        if fill:
            btn.grid(row=row, column=column, sticky='ew')
        else:
            btn.grid(row=row, column=column)
        return btn

    def _get_new_entry(self, row, column):
        '''
        This function returns a tk.Entry disabled by default,
        colored red with the text "None selected!".

        Parameters:
            - row: int
                The row index in the frame it will be placed in.
            - column: int
                The column index in the frame it will be placed in.
        '''
        new_entry = tk.Entry(self.frame, bg='red', width=75, bd=5)
        new_entry.insert(0, "None selected!")
        new_entry.config(state=tk.DISABLED)
        new_entry.grid(row=row, column=column)
        return new_entry

    def set_source(self):
        '''
        Gets the user to select a new input folder.
        If no directory is selected, the sort button
        is disabled and a corresponding error message
        is set in the status label.
        '''
        self.source = askdirectory()
        self.source_entry.config(state=tk.NORMAL)
        self.source_entry.delete(0, len(self.source_entry.get()))
        if not self.source:
            self.source = None
            self.source_entry.insert(0, "None selected!")
            self.source_entry.config(bg='red')
        else:
            self.source_entry.insert(0, self.source)
            self.source_entry.config(bg='green')
        self.source_entry.config(state=tk.DISABLED)
        self._check_execute()
    
    def set_dest(self):
        '''
        Gets the user to select a new output folder.
        If no directory is selected, the sort button
        is disabled and a corresponding error message
        is set in the status label.
        '''
        self.dest = askdirectory()
        self.dest_entry.config(state=tk.NORMAL)
        self.dest_entry.delete(0, len(self.source_entry.get()))
        if not self.dest:
            self.dest = None
            self.dest_entry.insert(0, "None selected!")
            self.dest_entry.config(bg='red')
        else:
            self.dest_entry.insert(0, self.dest)
            self.dest_entry.config(bg='green')
        self.dest_entry.config(state=tk.DISABLED)
        self._check_execute()

    def _check_execute(self):
        '''
        This function checks for a selected path for
        both the input and output directories. The sort
        button is only enabled if both the input and output
        folders are selected.
        '''
        if self.source and self.dest:
            self.status.config(text="Ready to sort!", bg='lightgreen')
            self.sort_btn.config(state=tk.NORMAL)
            return
        if self.source:
            self.status.config(text="No output folder selected!")
        elif self.dest:
            self.status.config(text="No input folder selected!")
        else:
            self.status.config(text="No folders selected!")
        self.status.config(bg='red')
        self.sort_btn.config(state=tk.DISABLED)

    def sort(self):
        '''
        This function starts the sorting process for all
        the files in the selected input folder.
        '''
        self.status.config(text="Checking for network connectivity...", bg='yellow')
        self.window.update()
        if pwfuncs.check_connection():
            self.status.config(text="Connected!", bg='lightgreen')
            self.window.update()
        else:
            self.status.config(text="No connection detected! Aborted!", bg='red')
            self.window.update()
            return
        cookies = pwfuncs.cookies
        if not cookies:
            self.status.config(text="Please login to your VT account!", bg='yellow')
            self.window.update()
        if not cookies:
            cookies = pwfuncs.get_login()
            if not cookies:
                self.status.config(text="Login Failed! Aborting!", bg='red')
                self.window.update()
                return
        self.status.config(text="Sorting...", bg='yellow')
        self.window.update()
        good_results = dict()
        bad_keys = []
        dupes = []
        pdf_files = sorted([filename for filename in os.listdir(self.source) if filename.endswith(".pdf")])

        keys, dirs = self._load_halls()
        if self.all_folders.get():
            for dir in dirs:
                os.makedirs(os.sep.join([self.dest, dir]), exist_ok=True)
        with sync_playwright() as pw:
            first_nav = True
            browser = pw.chromium.launch(headless=True)
            p = browser.new_page()
            p.context.add_cookies(cookies)
            pwfuncs.navigate_to_results(p)
            for index, filename in enumerate(pdf_files, start=1):
                if not pwfuncs.check_connection():
                    self.status.config("Connection Lost! Aborting...", bg='red')
                    self.window.update()
                    break
                sort_details = self._get_sort_details(filename, keys)
                if len(sort_details) == 1:
                    bad_keys.append(sort_details[0])
                    continue
                dest_folder = os.sep.join([self.dest, dirs[keys.index(sort_details[-1])]])
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                applicant_folder = os.sep.join([dest_folder, sort_details[0].strip()])
                if not os.path.exists(applicant_folder):
                    os.makedirs(applicant_folder)
                try:
                    os.rename(os.sep.join([self.source, filename]), os.sep.join([applicant_folder, f"{sort_details[0]} Hiring Documents.pdf"]))
                    if len(sort_details) == 3:
                        pwfuncs.get_survey(p, sort_details[1], os.sep.join([applicant_folder, f"{sort_details[0]} Scheduling Survey.pdf"]), new_navigation=first_nav)
                        first_nav = False
                    else:
                        sort_details.insert(1, -1)
                    good_results[index] = sort_details
                except OSError:
                    dupes.append(filename)
        result_str = "Sorting process complete!"
        if self.log.get():
            good_df = pd.DataFrame.from_dict(good_results, orient='index')
            good_df.rename(columns={0: "Name", 1: "Scheduling Survey Number", 2: "Dining Hall"}, inplace=True)
            dupe_df = pd.DataFrame(dupes, columns=['Duplicate Files'])
            bad_df = pd.DataFrame(bad_keys, columns=['Dining Hall Not Found'])
            save_path = f"{dt.now().strftime("%Y-%m-%d-%H-%M-%S")}.xlsx"
            with pd.ExcelWriter(f"{self.dest}/{save_path}", engine="openpyxl") as writer:
                good_df.to_excel(writer, index=False, sheet_name = "Sorted Applicants")
                bad_df.to_excel(writer, index=False, sheet_name = "Unsorted Files - No Hall")
                dupe_df.to_excel(writer, index=False, sheet_name = "Unsorted Files - Duplicates")
            result_str += f" View your results at {save_path}!"
        self.status.config(text=result_str, bg='lightgreen')
   
    def _get_sort_details(self, filename, keys):
        '''
        This function returns a list of details used
        to sort the provided file based on the filename.

        Parameters:
            - filename: str
                The name of the file to be sorted.
            - keys: List[str]
                The list of possible keys used to
                identify the dining hall the file
                should be sorted to.
        
        Returns:
            If a valid key is in the filename, one
            of two types of lists can be returned:
                - If a SSID is found, a 3-elem list
                  is returned.
                - If no SSID matches are found, a 
                  2-elem list is returned.
            If no valid key is found in the filename,
            the filename is returned as a 1-elem list
            containing only the filename.
        '''
        ssid_pattern = r"\s+\d+\s+"
        file_no_ext = filename[:-4].strip()
        if not any([file_no_ext.endswith(key) for key in keys]):
            return [filename]
        ssid_matches = re.findall(ssid_pattern, file_no_ext)
        if len(ssid_matches) > 0:
            details = file_no_ext.split(ssid_matches[0])
            details.insert(1, int(ssid_matches[0]))
            return details
        else:
            for key in keys:
                if file_no_ext.endswith(key):
                    name = file_no_ext[:-len(key)].strip()
                    return [name, key]

    def _load_halls(self):
        '''
        This function is a wrapper for loading the hall settings.
        To be used when the sort button is clicked, to retrieve
        the saved settings.
        '''
        keys = []
        dirs = []
        for _, keypairs in saves.get_saves().items():
            keys.append(keypairs[0])
            dirs.append(keypairs[1])
        return keys, dirs

    def start(self):
        '''
        This function is a wrapper for starting the
        Tk window in this class.
        '''
        self.window.mainloop()

if __name__ == "__main__":
    Organizer().start()