""" Explorer GUI """

import tkinter as tk

from .configuration import PRIMARY_BACKGROUND_COLOR
from .gui_frame import Frame


class ExplorerFrame(Frame):
    """The explorer frame"""

    def __init__(self, window, app):
        super().__init__(window, app)
        self.window = window
        self.app = app
        self.frame = tk.Frame(self.window, bg=PRIMARY_BACKGROUND_COLOR)

        self.collection = self.app.get_collection()

        # GUI

        self.show()

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()

    def set_collection(self, collection):
        """Set the actual collection"""
        self.collection = collection

    def load_collection(self):
        """Load the collection content in the frame"""
