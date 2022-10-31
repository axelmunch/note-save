""" Managing files and folders """

from os import makedirs, listdir, path
from .configuration import VALID_FILE_NAME_CHARACTERS


def create_full_path(dir_path):
    """ Create all the directories to a path """
    try:
        makedirs(dir_path, exist_ok=True)
    except OSError as error:
        print(f"Cannot create the folder.\n{error}")


def list_files(dir_path):
    """ Return a list of files and directories in a folder """
    if is_folder(dir_path):
        return listdir(dir_path)
    return []


def list_folders(dir_path):
    """ Return a list of folders in a folder """
    if is_folder(dir_path):
        return [element for element in list_files(dir_path) if is_folder(f"{dir_path}/{element}")]
    return []


def is_file(element_path):
    """ Return True if the path is a file, False otherwise """
    return path.isfile(element_path)


def is_folder(element_path):
    """ Return True if the path is a folder, False otherwise """
    return path.isdir(element_path)


def valid_file_name(text):
    """ Return True if the text is a valid file name, False otherwise """
    for char in text:
        if char not in VALID_FILE_NAME_CHARACTERS:
            return False
    return True
