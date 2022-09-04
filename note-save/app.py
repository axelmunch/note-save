from configuration import *
from gui_banner import *
from gui_input import *
from gui_explorer import *


class App:
    def __init__(self, root):
        self.root = root

        root.title("Note Save")

        self.collection = DEFAULT_COLLECTION_NAME

        # Banner
        self.banner_gui = Banner_frame(self.root, self)

        # Input
        self.input_gui = Input_frame(self.root, self)

        # Explorer
        self.explorer_gui = Explorer_frame(self.root, self)
        # Hide this frame by default
        self.explorer_gui.hide()

    def event_escape(self, inputs_cleared = False):
        # Event pressing escape

        # If everything is empty, close the window
        if inputs_cleared:
            self.root.destroy()

    def get_collection(self):
        return self.collection

    def set_collection(self, collection):
        self.collection = collection
        self.input_gui.set_collection(self.collection)
        # self.explorer_gui.set_collection(self.collection) # Uncomment when this GUI is implemented