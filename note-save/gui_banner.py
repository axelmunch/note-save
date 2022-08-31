# The top banner

from configuration import *
import tkinter as tk


class Banner_frame():
    def __init__(self, window, app):
        self.window = window
        self.app = app
        self.frame = tk.Frame(self.window, bg = BANNER_BACKGROUND_COLOR)

        # GUI
        self.label = tk.Label(self.frame, text = "Note Save")
        self.label.pack()

        self.show()

    def show(self):
        self.frame.pack(fill = tk.X)

    def hide(self):
        self.frame.pack_forget()