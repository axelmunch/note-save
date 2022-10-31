""" Explorer GUI """

import tkinter as tk
from .configuration import PRIMARY_BACKGROUND_COLOR
from .gui_frame import Frame


class ExplorerFrame(Frame):
    """ The explorer frame """

    def __init__(self, window, app):
        self.window = window
        self.app = app
        self.frame = tk.Frame(self.window, bg=PRIMARY_BACKGROUND_COLOR)

        # GUI

        self.show()

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()
