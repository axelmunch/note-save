""" Entry point of the application """

import tkinter as tk

from note_save.app import App

if __name__ == "__main__":
    root = tk.Tk()

    # GUI and events
    a = App(root)

    root.mainloop()

    del a
