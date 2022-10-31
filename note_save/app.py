""" GUI management and logic of the appplication """

from tkinter import TclError
from .configuration import DEFAULT_COLLECTION_NAME
from .gui_banner import BannerFrame
from .gui_input import InputFrame
from .gui_explorer import ExplorerFrame


class App:
    """ Class containing the navigation logic of the application """

    def __init__(self, root):
        self.root = root

        root.title("Note Save")
        try:
            root.iconbitmap("icon.ico")
        except TclError:
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

        # Hide the explorer frame by default
        self.explorer_gui.hide()

        # Ignore the events if a child window is open
        self.ignore_events = False

    def get_ignore_events(self):
        """ Return if the events should be ignored """
        return self.ignore_events

    def set_ignore_events(self, ignore_events):
        """ Set if the events should be ignored """
        self.ignore_events = ignore_events

    def event_escape(self, inputs_cleared=False):
        """ If the inputs are cleared and events are not ignored, exit the application """
        if not self.get_ignore_events() and inputs_cleared:
            self.root.destroy()

    def get_collection(self):
        """ Return the current collection """
        return self.collection

    def set_collection(self, collection):
        """ Set the current collection """
        self.collection = collection
        self.input_gui.set_collection(self.collection)
        # self.explorer_gui.set_collection(self.collection) # Uncomment when this GUI is implemented
