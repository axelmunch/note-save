"""GUI management and logic of the appplication"""

from tkinter import TclError

from .configuration import DEFAULT_COLLECTION_NAME
from .gui_banner import BannerFrame
from .gui_explorer import ExplorerFrame
from .gui_input import InputFrame
from .ui import UI


class App:
    """Class containing the navigation logic of the application"""

    def __init__(self, root):
        self.root = root

        root.title("Note Save")

        try:
            root.iconbitmap("note_save/icon.ico")
        except TclError as error:
            print(f"Cannot load icon.\n{error}")

        self.collection = DEFAULT_COLLECTION_NAME

        # Banner
        self.banner_gui = BannerFrame(self.root, self)

        # Input
        self.input_gui = InputFrame(self.root, self)

        # Explorer
        self.explorer_gui = ExplorerFrame(self.root, self)

        # Set the default UI to input
        self.change_ui(UI.INPUT)

        # Ignore the events if a child window is open
        self.set_ignore_events(False)

    def switch_ui(self):
        """Switch UI to Input or Explorer"""
        if self.current_ui == UI.INPUT:
            self.change_ui(UI.EXPLORER)
        elif self.current_ui == UI.EXPLORER:
            self.change_ui(UI.INPUT)

    def change_ui(self, new_ui):
        """Change the current UI and set the others invisible"""
        self.current_ui = new_ui
        match self.current_ui:
            case UI.INPUT:
                self.banner_gui.set_switch_ui_text("Explore")
                self.input_gui.show()
                self.explorer_gui.hide()
            case UI.EXPLORER:
                self.banner_gui.set_switch_ui_text("Input")
                self.input_gui.hide()
                self.explorer_gui.show()
                self.explorer_gui.full_refresh()

        self.resize()

    def resize(self):
        """Resize the window"""
        self.root.geometry("")
        self.root.minsize(0, 0)
        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())

    def get_ignore_events(self):
        """Return if the events should be ignored"""
        return self.ignore_events

    def set_ignore_events(self, ignore_events):
        """Set if the events should be ignored"""
        self.ignore_events = ignore_events

    def event_escape(self, inputs_cleared=False):
        """If the inputs are cleared and events are not ignored, exit the application"""
        if not self.get_ignore_events() and inputs_cleared:
            self.root.destroy()

    def get_collection(self):
        """Return the current collection"""
        return self.collection

    def set_collection(self, collection):
        """Set the current collection"""
        self.collection = collection
        self.input_gui.set_collection(self.collection)
        self.explorer_gui.set_collection(self.collection)

    def add_to_clipboard(self, content):
        """Add content to the clipboard"""
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
