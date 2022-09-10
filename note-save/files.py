from configuration import *
from os import makedirs, listdir, path


def create_full_path(dir_path):
    # Create all the directories a full path
    makedirs(dir_path, exist_ok = True)

def list_files(dir_path):
    # Return a list of files and directories in a folder
    if is_folder(dir_path):
        return listdir(dir_path)
    return None

def list_folders(dir_path):
    # Return a list of folders in a folder
    if is_folder(dir_path):
        return [element for element in list_files(dir_path) if is_folder(f"{dir_path}/{element}")]
    return None

def is_file(element_path):
    # Return True if the path is a file, False otherwise
    return path.isfile(element_path)

def is_folder(element_path):
    # Return True if the path is a folder, False otherwise
    return path.isdir(element_path)

def valid_file_name(text):
    for char in text:
        if char not in VALID_FILE_NAME_CHARACTERS:
            return False
    return True