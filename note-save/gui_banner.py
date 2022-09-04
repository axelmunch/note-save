# The top banner

from configuration import *
from files import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


class Banner_frame():
    def __init__(self, window, app):
        self.window = window
        self.app = app
        self.frame = tk.Frame(self.window, bg = BANNER_BACKGROUND_COLOR)

        self.collection = self.app.get_collection()

        # GUI
        self.label = tk.Label(self.frame, text = "Note Save")
        self.label.pack()

        self.combobox = ttk.Combobox(self.frame, state = "readonly")
        self.load_collections()
        self.combobox.set(self.collection)
        self.combobox.pack()
        self.combobox.bind("<<ComboboxSelected>>", self.change_collection)

        self.show()

    def load_collections(self):
        folders = list_folders(SAVE_FOLDER)
        if DEFAULT_COLLECTION_NAME not in folders:
            folders.append(DEFAULT_COLLECTION_NAME)
        if folders != None:
            self.combobox["values"] = folders
        else:
            self.combobox["values"] = [DEFAULT_COLLECTION_NAME]

    def change_collection(self, event = None):
        self.collection = self.combobox.get()
        # Set the collection in the app for the others GUIs
        self.app.set_collection(self.collection)

    def add_collection(self, collection):
        # Create the directory
        create_full_path(f"{SAVE_FOLDER}/{collection}")
        # Reload the collections
        self.load_collections()
        # Set the new collection
        self.combobox.set(collection)
        # Trigger the collection change event
        self.change_collection()

    def show(self):
        self.frame.pack(fill = tk.X)

    def hide(self):
        self.frame.pack_forget()