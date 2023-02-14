"""Top banner GUI"""

import tkinter as tk
from tkinter import TclError, messagebox, ttk

from .configuration import (
    BANNER_BACKGROUND_COLOR,
    DEFAULT_COLLECTION_NAME,
    DEFAULT_PADDING,
    PRIMARY_BACKGROUND_COLOR,
    SAVE_FOLDER,
    TEXT_COLOR,
    VALID_FILE_NAME_PATTERN,
)
from .files import create_full_path, list_folders, open_file_explorer, valid_file_name
from .gui_frame import Frame


class BannerFrame(Frame):
    """The top banner with navigation"""

    def __init__(self, window, app):
        super().__init__(window, app)
        self.app = app
        self.frame = tk.Frame(window, bg=BANNER_BACKGROUND_COLOR)

        self.collection = self.app.get_collection()

        self.new_collection_window = None
        self.new_collection_input = None

        # GUI
        self.label = tk.Label(
            self.frame,
            text="Note Save",
            bg=BANNER_BACKGROUND_COLOR,
            fg=TEXT_COLOR,
        )
        self.label.pack()

        self.combobox = ttk.Combobox(self.frame, state="readonly")
        self.load_collections()
        self.combobox.set(self.collection)
        self.combobox.pack(pady=DEFAULT_PADDING)
        self.combobox.bind("<<ComboboxSelected>>", self.event_change_collection)

        self.add_button = tk.Button(self.frame, text="+", command=self.event_button_add)
        self.add_button.pack(pady=DEFAULT_PADDING)

        self.open_button = tk.Button(
            self.frame, text="Open", command=self.event_open_collection
        )
        self.open_button.pack(pady=DEFAULT_PADDING)

        self.switch_ui_button = tk.Button(self.frame, command=self.event_switch_ui)
        self.switch_ui_button.pack(pady=DEFAULT_PADDING)

        self.show()

    def show(self):
        self.frame.pack(fill=tk.X)

    def hide(self):
        self.frame.pack_forget()

    def event_open_collection(self, event=None):
        """Open the collection folder"""
        del event
        try:
            open_file_explorer(f"{SAVE_FOLDER}/{self.collection}")
        except FileNotFoundError as error:
            messagebox.showwarning(
                title="Warning",
                message="This collection cannot be opened because it has not "
                f"been created yet.\nTry to add something to it.\n{error}",
            )

    def event_switch_ui(self, event=None):
        """Switch UI"""
        del event
        self.app.switch_ui()

    def event_button_add(self, event=None):
        """Open a child window to ask for the name of the new collection"""
        del event
        self.new_collection_window = tk.Toplevel(bg=PRIMARY_BACKGROUND_COLOR)
        self.new_collection_window.title("Create a collection")
        try:
            self.new_collection_window.iconbitmap("note_save/icon.ico")
        except TclError as error:
            print(f"Cannot load icon.\n{error}")
        # Title label
        label = tk.Label(
            self.new_collection_window,
            text="Enter a name for the collection",
            bg=PRIMARY_BACKGROUND_COLOR,
            fg=TEXT_COLOR,
        )
        label.pack(padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
        # Input text
        self.new_collection_input = tk.Text(
            self.new_collection_window, width=1, height=1, wrap=None
        )
        self.new_collection_input.pack(
            fill=tk.BOTH,
            expand=True,
            padx=DEFAULT_PADDING,
            pady=DEFAULT_PADDING,
        )
        self.new_collection_input.focus_set()
        self.new_collection_input.bind("<Key>", self.event_typing_valid)
        self.new_collection_input.bind("<Return>", self.event_enter_collection_name)
        # Ok button
        button_ok = tk.Button(
            self.new_collection_window,
            text="Create",
            command=self.event_enter_collection_name,
        )
        button_ok.pack(padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)

        self.new_collection_window.resizable(False, False)

        # Ignore other events while this window is opened
        self.app.set_ignore_events(True)

        self.new_collection_window.protocol(
            "WM_DELETE_WINDOW", self.event_close_collection_window
        )

        self.new_collection_window.grab_set()

    def event_typing_valid(self, event):
        """Only allow ASCII characters when typing"""
        if len(event.char) == 1 and ord(event.char) > 127:
            return "break"
        return True

    def event_close_collection_window(self, event=None):
        """Close the child window"""
        del event
        if self.new_collection_window is not None:
            self.new_collection_window.destroy()
        self.new_collection_input = None
        self.app.set_ignore_events(False)

    def event_enter_collection_name(self, event=None):
        """Enter a new name for a collection"""
        del event
        if self.new_collection_input is not None:
            # Get the text
            collection_name = self.new_collection_input.get("1.0", "end-1c").strip()
            self.new_collection_input.delete("1.0", tk.END)
            self.new_collection_input.insert(tk.END, collection_name)
            # If the collection is a valid file name
            if valid_file_name(collection_name) and len(collection_name) > 0:
                # Add the collection
                self.add_collection(collection_name)
                # Close the window
                self.event_close_collection_window()
            else:
                messagebox.showerror(
                    title="Error",
                    message="The collection name must be a valid file name.\n"
                    f"{collection_name} doesn't respect "
                    f"{VALID_FILE_NAME_PATTERN}",
                )
        # Don't add new line character if return is pressed
        return "break"

    def event_escape(self):
        """Close new collection window if opened"""
        self.event_close_collection_window()

    def load_collections(self):
        """Load the collections name list from the save folder"""
        folders = list_folders(SAVE_FOLDER)
        if DEFAULT_COLLECTION_NAME not in folders:
            folders = [DEFAULT_COLLECTION_NAME] + folders
        if len(folders) > 0:
            self.combobox["values"] = folders
        else:
            self.combobox["values"] = [DEFAULT_COLLECTION_NAME]

    def event_change_collection(self, event=None):
        """Changing the collection this GUI"""
        del event
        self.collection = self.combobox.get()
        # Set the collection in the app for the others GUIs
        self.app.set_collection(self.collection)

    def add_collection(self, collection):
        """Creating a new collection"""

        # Create the directory
        create_full_path(f"{SAVE_FOLDER}/{collection}")
        # Reload the collections
        self.load_collections()
        # Set the new collection
        self.combobox.set(collection)
        # Trigger the collection change event
        self.event_change_collection()

    def set_switch_ui_text(self, text):
        """Set the Switch UI label text"""
        self.switch_ui_button.config(text=text)
