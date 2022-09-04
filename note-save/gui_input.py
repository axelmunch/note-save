# The main frame with inputs

from configuration import *
from save import *
from clipboard_image import *
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk


class Input_frame():
    def __init__(self, window, app):
        self.window = window
        self.app = app
        self.frame = tk.Frame(self.window, bg = "red")

        self.frame.bind_all("<<Paste>>", self.event_paste)
        self.frame.bind_all("<Escape>", self.event_escape)
        self.frame.bind_all("<Return>", self.event_enter)

        # Attachments
        self.images = []
        # Instances of the Image_frame class
        self.image_cache = []

        self.text = ""

        self.collection = self.app.get_collection()

        # GUI
        self.image_container = tk.Frame(self.frame, bg = "yellow")
        self.image_container.pack(fill = tk.BOTH, expand = True, padx = DEFAULT_PADDING, pady = DEFAULT_PADDING)

        self.label_image_container = tk.Label(self.image_container)
        self.label_image_container.pack(anchor = tk.NW, padx = DEFAULT_PADDING, pady = DEFAULT_PADDING)

        self.textbox = scrolledtext.ScrolledText(self.frame, wrap = tk.WORD, height = TEXT_LINE_HEIGHT)
        self.textbox.pack(fill = tk.X, expand = True, side = tk.LEFT, padx = DEFAULT_PADDING, pady = DEFAULT_PADDING)
        self.textbox.focus_set()

        self.button_save = tk.Button(self.frame, text = "Save", command = self.event_save)
        self.button_save.pack(side = tk.RIGHT, padx = DEFAULT_PADDING, pady = DEFAULT_PADDING)

        self.show()

    def show(self):
        self.frame.pack(fill = tk.BOTH, expand = True)

    def hide(self):
        self.frame.pack_forget()

    def get_text(self):
        self.text = self.textbox.get("1.0", "end-1c")

    def clear_text(self):
        # Remove the text inside the textbox
        self.textbox.delete("1.0", tk.END)
        # Reset the text variable
        self.get_text()

    def set_collection(self, collection):
        self.collection = collection

    def is_text_empty(self):
        # Return True if the text is empty or contains only whitespace characters, False otherwise
        return len(self.text) == 0 or self.text.isspace()

    def inputs_cleared(self):
        # Return True if all inputs are cleared, False otherwise
        return self.is_text_empty() and len(self.images) == 0

    def event_escape(self, event = None):
        # Get the text in the input
        self.get_text()

        # If everything is empty before resetting, it will close the app
        inputs_cleared = self.inputs_cleared()
        # Clear the inputs
        self.reset_inputs()

        self.app.event_escape(inputs_cleared)

    def event_paste(self, event = None):
        # Something is pasted in the window, if it is images, add them to the list of images
        self.images += get_clipboard_images()
        if len(self.images) > 0:
            # Update the images on the screen
            self.image_update()

    def event_enter(self, event = None):
        self.get_text()
        # If the text is empty or contains only whitespace characters and there is at least one image, trigger the save event
        if self.is_text_empty() and len(self.images) > 0:
            self.event_save()

    def event_save(self):
        # Saving the inputs

        # Set the text variable to the input text
        self.get_text()
        # If the text is empty or contains only whitespace characters, delete the text
        if self.is_text_empty():
            self.clear_text()
        # Saving
        if len(self.text) > 0 or len(self.images) > 0:
            save(self.collection, self.text, self.images)
        # Reset the inputs
        self.reset_inputs(True)

    def reset_inputs(self, full = False):
        # Reset the inputs, by first resetting the images, then the text. Or resetting everything for a full reset

        if full:
            # Clear everything
            self.images = []
            self.image_update()
            self.clear_text()
        elif len(self.images) > 0:
            # Clear the images first if there are any
            self.images = []
            self.image_update()
        else:
            # Clear the text when there is no images
            self.clear_text()

    def set_label_images(self):
        # Set the label text, images and quantity or nothing
        self.label_image_container.config(text = f"Images {len(self.images)}" * (len(self.images) > 0))

    def delete_image(self, image):
        self.images.remove(image)
        # Update the label containing the number of images
        self.set_label_images()

    def image_update(self):
        # Display the images in the image_container

        # Update the label containing the number of images
        self.set_label_images()

        # Delete actual images
        for image in self.image_cache:
            image.hide()
            del image

        # Reset the image cache
        self.image_cache = []

        # Display the images
        for image in self.images:
            self.image_cache.append(Image_frame(self.image_container, image, self.delete_image))

class Image_frame():
    def __init__(self, parent, image, delete_image_function):
        self.parent = parent
        self.image = image

        # Function to delete an image
        self.delete_image_function = delete_image_function

        # Create a container for the image
        self.frame = tk.Frame(self.parent)

        # Resize the image with the size limit (keeping ratio)
        image_width = self.image.width
        image_height = self.image.height

        if image_width > image_height:
            resize_width = MAX_PREVIEW_IMAGE_SIZE
            resize_height = int(image_height / (image_width / MAX_PREVIEW_IMAGE_SIZE))
        else:
            resize_height = MAX_PREVIEW_IMAGE_SIZE
            resize_width = int(image_width / (image_height / MAX_PREVIEW_IMAGE_SIZE))

        image_resized = self.image.resize((resize_width, resize_height), Image.ANTIALIAS)

        # Convert the image for Tkinter
        self.display_image = ImageTk.PhotoImage(image_resized)

        # Add the image with the delete click event
        button_image = tk.Button(self.frame, image = self.display_image, command = self.delete)
        button_image.pack()

        self.show()

    def delete(self):
        self.delete_image_function(self.image)
        self.hide()

    def show(self):
        self.frame.pack()
        # self.frame.grid()

    def hide(self):
        self.frame.pack_forget()