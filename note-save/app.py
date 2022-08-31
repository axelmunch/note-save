from configuration import *
from save import *
from image import *
from gui_banner import *
from gui_input import *
from gui_explorer import *


class App:
    def __init__(self, root):
        self.root = root

        root.title("Note Save")

        self.images = []
        self.text = ""

        self.collection = DEFAULT_COLLECTION_NAME

        # Banner
        self.banner_gui = Banner_frame(self.root, self)

        # Input
        self.input_gui = Input_frame(self.root, self)

        # Explorer
        self.explorer_gui = Explorer_frame(self.root, self)
        # Hide this frame by default
        self.explorer_gui.hide()

    def paste(self):
        images = get_clipboard_images()
        for image in images:
            self.images.append(image)
        if len(images) > 0:
            # Send the new images to the input frame
            self.input_gui.image_update(self.images)

    def escape(self):
        # Event pressing escape

        # If everything is empty, close the window
        if self.input_gui.get_text() == "" and len(self.images) == 0:
            self.root.quit()
        self.reset_inputs()

    def set_text(self, text):
        self.text = text

    def save(self):
        # Saving the inputs

        save(self.collection, self.text, self.images)
        self.reset_inputs(True)

    def delete_image(self, image, image_update = False):
        self.images.remove(image)
        if image_update:
            self.input_gui.image_update(self.images)

    def reset_inputs(self, full = False):
        if full:
            self.images = []
            self.input_gui.image_update(self.images)
            self.input_gui.clear_text()
        elif len(self.images) > 0:
            self.images = []
            self.input_gui.image_update(self.images)
        else:
            self.input_gui.clear_text()