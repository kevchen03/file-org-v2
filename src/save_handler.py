import os, tempfile, json

tmpdir = tempfile.gettempdir()
save_folder = f"{tmpdir}/FileOrganizerUserInfo"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)
save_file = f"{save_folder}/save_info.json"
if not os.path.exists(save_file):
    with open(save_file, 'w', encoding='utf-8') as saves:
        json.dump(dict(), saves, ensure_ascii=False, indent=4)

def get_saves():
    '''
    This function retrieves the user's local data
    as a dictionary.
    '''
    with open(save_file, 'r', encoding='utf-8') as in_file:
        return json.load(in_file)

def post_saves(save_data):
    '''
    This function saves the user's settings to
    the local storage.
    '''
    with open(save_file, 'w', encoding='utf-8') as out_file:
        json.dump(save_data, out_file, ensure_ascii=False, indent=4)