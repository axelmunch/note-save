# The main frame with inputs

from configuration import *
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk


class Input_frame():
    def __init__(self, window, app):
        self.window = window
        self.app = app
        self.frame = tk.Frame(self.window, bg = "red")

        self.frame.bind_all("<<Paste>>", self.paste)
        self.frame.bind_all("<Escape>", self.escape)

        # Actual images, to be displayed
        self.images = []
        # Instances of the Image_frame class
        self.image_cache = []

        # GUI
        self.image_container = tk.Frame(self.frame, bg = "yellow")
        self.image_container.pack(fill = tk.BOTH, expand = True, padx = DEFAULT_PADDING, pady = DEFAULT_PADDING)

        self.label_image_container = tk.Label(self.image_container)
        self.label_image_container.pack(side = tk.LEFT)

        self.textbox = scrolledtext.ScrolledText(self.frame, wrap = tk.WORD, height = TEXT_LINE_HEIGHT)
        self.textbox.pack(side = tk.LEFT, padx = DEFAULT_PADDING, pady = DEFAULT_PADDING)
        self.textbox.focus_set()

        self.button_save = tk.Button(self.frame, text = "Save", command = self.save)
        self.button_save.pack(side = tk.RIGHT, padx = DEFAULT_PADDING, pady = DEFAULT_PADDING)

        self.show()

    def show(self):
        self.frame.pack(fill = tk.BOTH, expand = True)

    def hide(self):
        self.frame.pack_forget()

    def get_text(self):
        return self.textbox.get("1.0", "end-1c")

    def save(self):
        # Send text to app
        self.app.set_text(self.get_text())
        self.clear_text()
        # Save content event in app
        self.app.save()

    def paste(self, event = None):
        self.app.paste()

    def escape(self, event = None):
        self.app.escape()

    def set_label_images(self):
        # Set label text, images and quantity or nothing
        self.label_image_container.config(text = f"Images {len(self.images)}" * (len(self.images) > 0))

    def image_update(self, images):
        self.images = images

        # Delete actual images
        for image in self.image_cache:
            image.hide()
            del image

        self.image_cache = []

        self.set_label_images()

        # Display the images
        for image in self.images:
            self.image_cache.append(Image_frame(self.image_container, image, self.app, self.set_label_images))

    def clear_text(self):
        # Remove the text inside the textbox
        self.textbox.delete("1.0", tk.END)

class Image_frame():
    def __init__(self, parent, image, app, update_label_function):
        self.app = app
        self.parent = parent
        self.image = image

        # To update the image count when deleting an image
        self.update_label_function = update_label_function

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
        self.app.delete_image(self.image)
        self.hide()
        self.update_label_function()

    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()