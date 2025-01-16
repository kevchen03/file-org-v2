# Welcome to the File Organizer App!
```
Author: Kevin Chen
Last Updated: Jan. 16, 2025
```

## Introduction
This `README.md` assumes you are currently in the `file-org-v2/` directory, where everything in this project is contained. For information regarding Version 1 of this project, please navigate to `file-org-v1/`.

## `venv` Setup and Activation
This project was created on a Windows 10 platform using Python 3.12.7, with Git Bash as the main CLI. 

To create the virtual environment, run:
```sh
python -m venv venv
```

To activate the virtual environment, please run the command:
```sh
source venv/Scripts/activate
```

To deactivate it, simply run the following command in the terminal:

```sh
 deactivate
```

Finally, to destroy the `venv`, simply run
```sh
rm -rf venv
```

## `venv` Packages
This environment has the following packages installed:
- `playwright`: for access to a chromium browser and therefore Microsoft Forms
```sh
pip install playwright;
playwright install;
```
- `tk`: for the app GUI
```sh
pip install tk;
```
- `pandas`: for data manipulation
```sh
pip install pandas;
```
- `openpyxl`: for pandas writing out to excel files
```sh
pip install openpyxl;
```
- `pyinstaller`: for compiling the application
```sh
pip install pyinstaller;
```

This project also makes use of the following native libraries:
- `copy` - for deepcopying structures
- `datetime` - for user-friendly logging
- `http` - for verifying internet connections
- `json` - for accessing user data stored in `json` format
- `os` - for making files and directories
- `re` - for regex pattern matching
- `tempfile` - for access to the Temp folder to store user data

## Directory Structure
The source code for this project all lies in the `src/` directory. The source scripts are as follows:
- `main.py`: contains the main running code to pull up an Organizer window.
- `OrganizerTk.py`: contains the class wrapping the Organizer window and all necessary methods.
- `HallManagerTk.py`: contains the class wrapping the window given to users to modify their hall settings.
- `playwright_funcs.py`: contains helper functions used to access the Scheduling Surveys from Microsoft Forms.
- `save_handler.py`: contains helper functions to access and modify the local user settings for hall data.
- `validator.py`: contains helper functions to validate strings for uniqueness and lack of illegal characters.
- `icon.ico`: the icon to be used for the application.

## Packaging the Executable
When compiling, first navigate to the `src/` directory before running. The compile commands for the executable are the following:
```sh
PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium
pyinstaller -w -F --icon "icon.ico" --name "FileOrganizer" main.py
```
The lines do the following:
- `PLAYWRIGHT_BROWSERS_PATH=0 playwright install chromium`: installs the chromium browser in the environment for packaging
- `pyinstaller -w -F --icon "icon.ico" --name "FileOrganizer" main.py`: compiles the executable with the entry point at `main.py`. Notes:
    - `-w`: compiles the executable to hide the command line interface.
    - `-F`: compiles the executable to be a single file instead of a directory
    - `--icon`: Sets the icon of the executable to the following argument, in this case the file `icon.ico`
    - `--name`: Sets the name of the executable to the following argument, in this case "FileOrganizer.exe"

Once compiled, the necessary files for packaging the executable will be created in the `src/` directory. They are:
- `build/`: Contains the executable and additional file details to be packaged.
- `dist/`: The directory containing the packaged executable on successful completion.
- `FileOrganizer.spec`: Contains more information about the executable.

## 
This project is meant solely for the Virginia Tech Dining Services Central Hiring Office, to aid in the process of gathering and sorting the necessary Student Applicant files. Note that this project works only on the assumption that the same Microsoft form is used, and that Microsoft Forms will continue to use the same HTML layout for their page.