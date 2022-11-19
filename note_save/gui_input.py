""" Main GUI """

import tkinter as tk
from tkinter import scrolledtext

from PIL import Image, ImageTk

from .clipboard_image import get_clipboard_images
from .configuration import (
    DEFAULT_PADDING,
    MAX_PREVIEW_IMAGE_SIZE,
    PRIMARY_BACKGROUND_COLOR,
    SECONDARY_BACKGROUND_COLOR,
    TEXT_COLOR,
    TEXT_LINE_HEIGHT,
)
from .gui_frame import Frame
from .save import save


class InputFrame(Frame):
    """The main frame with inputs"""

    def __init__(self, window, app):
        super().__init__(window, app)
        self.window = window
        self.app = app
        self.frame = tk.Frame(self.window, bg=PRIMARY_BACKGROUND_COLOR)

        self.frame.bind_all("<<Paste>>", self.event_paste)
        self.frame.bind_all("<Escape>", self.event_escape)
        self.frame.bind_all("<Return>", self.event_save)
        self.frame.bind_all("<Shift-Return>", self.event_enter)

        # Attachments
        self.images = []
        # Instances of the ImageFrame class
        self.image_cache = []

        self.text = ""

        self.collection = self.app.get_collection()

        # GUI
        self.image_container = tk.Frame(
            self.frame, bg=SECONDARY_BACKGROUND_COLOR
        )
        self.image_container.pack(
            fill=tk.BOTH,
            expand=True,
            padx=DEFAULT_PADDING,
            pady=DEFAULT_PADDING,
        )

        self.label_image_container = tk.Label(
            self.image_container, bg=SECONDARY_BACKGROUND_COLOR, fg=TEXT_COLOR
        )
        self.label_image_container.pack(
            anchor=tk.NW, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING
        )

        self.textbox = scrolledtext.ScrolledText(
            self.frame, wrap=tk.WORD, height=TEXT_LINE_HEIGHT
        )
        self.textbox.pack(
            fill=tk.X,
            expand=True,
            side=tk.LEFT,
            padx=DEFAULT_PADDING,
            pady=DEFAULT_PADDING,
        )
        self.textbox.focus_set()

        self.button_save = tk.Button(
            self.frame, text="Save", command=self.event_save
        )
        self.button_save.pack(
            side=tk.RIGHT, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING
        )

        self.show()

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()

    def get_text(self):
        """Get the text from the textbox without the
        whitespaces at the beginning and the end"""
        self.text = self.clear_whitespace(self.textbox.get("1.0", "end-1c"))

    def clear_text(self):
        """Remove the text inside the textbox"""
        self.textbox.delete("1.0", tk.END)
        # Reset the text variable
        self.get_text()

    def set_collection(self, collection):
        """Set the actual collection"""
        self.collection = collection

    def is_text_empty(self):
        """Return True if the text is empty"""
        return len(self.text) == 0

    def clear_whitespace(self, text):
        """Remove the whitespace characters at
        the beginning and the end of the text"""
        return text.strip()

    def inputs_cleared(self):
        """Return True if all inputs are cleared, False otherwise"""
        return self.is_text_empty() and len(self.images) == 0

    def event_escape(self, event=None):
        """When the escape key is pressed,
        reset the inputs or exit the application"""
        del event
        if not self.app.get_ignore_events():
            # Get the text in the input
            self.get_text()

            # If everything is empty before resetting, it will close the app
            inputs_cleared = self.inputs_cleared()
            # Clear the inputs
            self.reset_inputs()

            self.app.event_escape(inputs_cleared)

    def event_paste(self, event=None):
        """Something is pasted in the window"""
        del event
        if not self.app.get_ignore_events():
            # If it is images, add them to the list of images
            self.images += get_clipboard_images()
            if len(self.images) > 0:
                # Update the images on the screen
                self.image_update()

    def event_enter(self, event=None):
        """The enter key is pressed"""
        del event
        if not self.app.get_ignore_events():
            self.get_text()
            # If the text is empty and there is at least
            # one image, trigger the save event
            if self.is_text_empty() and len(self.images) > 0:
                self.event_save()

    def event_save(self, event=None):
        """Saving the inputs"""
        del event
        if not self.app.get_ignore_events():
            # Set the text variable to the input text
            self.get_text()
            # Saving
            saved = False
            if not self.is_text_empty() or len(self.images) > 0:
                saved = save(self.collection, self.text, self.images)
            # Reset the inputs
            if saved:
                self.reset_inputs(True)

    def reset_inputs(self, full=False):
        """Reset the inputs in two steps or reset everything"""
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
        """Set the label text, quantity of images or nothing"""
        self.label_image_container.config(
            text=f"Images {len(self.images)}" * (len(self.images) > 0)
        )

    def delete_image(self, image):
        """Delete an image from the list of images
        and update the label on the screen"""
        self.images.remove(image)
        # Update the label containing the number of images
        self.set_label_images()

    def image_update(self):
        """Display the images in the image container"""

        # Update the label containing the number of images
        self.set_label_images()

        # Delete actual images
        for widget in self.image_container.winfo_children():
            if not isinstance(widget, tk.Label):
                widget.destroy()

        # Reset the image cache
        self.image_cache = []

        # Display the images
        for image in self.images:
            self.image_cache.append(
                ImageFrame(self.image_container, image, self.delete_image)
            )


class ImageFrame:
    """An image container with a delete button"""

    def __init__(self, parent, image, delete_image_function):
        self.parent = parent
        self.image = image

        # Function to delete the image
        self.delete_image_function = delete_image_function

        # Create a container for the image
        self.frame = tk.Frame(self.parent)

        # Resize the image with the size limit (keeping ratio)
        image_width = self.image.width
        image_height = self.image.height
        if image_width > image_height:
            resize_width = MAX_PREVIEW_IMAGE_SIZE
            resize_height = int(
                image_height / (image_width / MAX_PREVIEW_IMAGE_SIZE)
            )
        else:
            resize_height = MAX_PREVIEW_IMAGE_SIZE
            resize_width = int(
                image_width / (image_height / MAX_PREVIEW_IMAGE_SIZE)
            )
        image_resized = self.image.resize(
            (resize_width, resize_height), Image.ANTIALIAS
        )

        # Convert the image for Tkinter
        self.display_image = ImageTk.PhotoImage(image_resized)

        # Add the image with the delete click event
        button_image = tk.Button(
            self.frame, image=self.display_image, command=self.delete
        )
        button_image.pack()

        self.show()

    def delete(self):
        """Delete the image"""
        self.delete_image_function(self.image)
        self.image = None
        self.display_image = None
        self.hide()

    def show(self):
        """Show the image container"""
        self.frame.pack()
        # self.frame.grid()

    def hide(self):
        """Hide the image container"""
        self.frame.pack_forget()
