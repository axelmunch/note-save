# The top banner

from .configuration import *
from .files import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Banner_frame():
    def __init__(self, window, app):
        self.window = window
        self.app = app
        self.frame = tk.Frame(self.window, bg = BANNER_BACKGROUND_COLOR)

        self.collection = self.app.get_collection()

        self.new_collection_input = None

        # GUI
        self.label = tk.Label(self.frame, text = "Note Save", bg = BANNER_BACKGROUND_COLOR, fg = TEXT_COLOR)
        self.label.pack()

        self.combobox = ttk.Combobox(self.frame, state = "readonly")
        self.load_collections()
        self.combobox.set(self.collection)
        self.combobox.pack(padx = DEFAULT_PADDING, pady = DEFAULT_PADDING)
        self.combobox.bind("<<ComboboxSelected>>", self.event_change_collection)

        self.add_button = tk.Button(self.frame, text = '+', command = self.event_button_add)
        self.add_button.pack(padx = DEFAULT_PADDING, pady = DEFAULT_PADDING)

        self.show()

    def show(self):
        self.frame.pack(fill = tk.X)

    def hide(self):
        self.frame.pack_forget()

    def event_button_add(self, event = None):
        # Open a child window to ask for the name of the new collection
        self.new_collection_window = tk.Toplevel(bg = PRIMARY_BACKGROUND_COLOR)
        self.new_collection_window.title("Create a collection")
        # Title label
        label = tk.Label(self.new_collection_window, text = "Enter a name for the collection", bg = PRIMARY_BACKGROUND_COLOR, fg = TEXT_COLOR)
        label.pack(padx = DEFAULT_PADDING, pady = DEFAULT_PADDING)
        # Input text
        self.new_collection_input = tk.Text(self.new_collection_window, width = 1, height = 1, wrap = None)
        self.new_collection_input.pack(fill = tk.BOTH, expand = True, padx = DEFAULT_PADDING, pady = DEFAULT_PADDING)
        self.new_collection_input.focus_set()
        self.new_collection_input.bind("<Key>", self.event_type_text_no_whitespace)
        # Ok button
        button_ok = tk.Button(self.new_collection_window, text = "Create", command = self.event_enter_collection_name)
        button_ok.pack(padx = DEFAULT_PADDING, pady = DEFAULT_PADDING)

        self.new_collection_window.resizable(False, False)

        # Ignore other events while this window is opened
        self.app.set_ignore_events(True)

        self.new_collection_window.protocol("WM_DELETE_WINDOW", self.event_close_collection_window)

        self.new_collection_window.grab_set()

    def event_type_text_no_whitespace(self, event):
        # Don't allow whitespace characters
        if event.char.isspace():
            return "break"

    def event_close_collection_window(self, event = None):
        self.new_collection_window.destroy()
        self.new_collection_input = None
        self.app.set_ignore_events(False)

    def event_enter_collection_name(self, event = None):
        if self.new_collection_input != None:
            # Get the text
            collection_name = self.new_collection_input.get("1.0", "end-1c").strip()
            # If the collection is a valid file name
            if valid_file_name(collection_name) and len(collection_name) > 0:
                # Add the collection
                self.add_collection(collection_name)
                # Close the window
                self.event_close_collection_window()
            else:
                messagebox.showerror(title = "Error", message = f"The collection name must be a valid file name ({collection_name})")

    def load_collections(self):
        folders = list_folders(SAVE_FOLDER)
        if DEFAULT_COLLECTION_NAME not in folders:
            folders.append(DEFAULT_COLLECTION_NAME)
        if len(folders) > 0:
            self.combobox["values"] = folders
        else:
            self.combobox["values"] = [DEFAULT_COLLECTION_NAME]

    def event_change_collection(self, event = None):
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
        self.event_change_collection()