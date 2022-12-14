"""Explorer GUI"""

import tkinter as tk
from math import ceil

from PIL import Image, ImageTk

from .configuration import (
    DEFAULT_PADDING,
    EXPLORER_MAX_BY_PAGE,
    IMAGE_EXTENSION,
    MAX_PREVIEW_IMAGE_SIZE,
    PREVIEW_IMAGES_BY_LINE,
    PRIMARY_BACKGROUND_COLOR,
    SAVE_FOLDER,
    SECONDARY_BACKGROUND_COLOR,
    TEXT_COLOR,
)
from .files import open_file
from .gui_frame import Frame
from .load import load


class ExplorerFrame(Frame):
    """The explorer frame"""

    def __init__(self, window, app):
        super().__init__(window, app)
        self.app = app
        self.frame = tk.Frame(window, bg=PRIMARY_BACKGROUND_COLOR)

        self.collection = self.app.get_collection()

        self.collection_content = []
        self.collection_page = 0
        self.content_cache = []

        # GUI

        # Page navigation
        self.controls_frame = tk.Frame(self.frame, bg=PRIMARY_BACKGROUND_COLOR)
        self.controls_frame.pack(fill=tk.X, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)

        tk.Label(
            self.controls_frame, text="Page", bg=PRIMARY_BACKGROUND_COLOR, fg=TEXT_COLOR
        ).grid(row=0, column=2)

        self.first_page_button = tk.Button(
            self.controls_frame, text="<<", command=self.first_page
        )
        self.first_page_button.grid(row=1, column=0)

        self.previous_page_button = tk.Button(
            self.controls_frame, text="<", command=self.previous_page
        )
        self.previous_page_button.grid(row=1, column=1, padx=DEFAULT_PADDING)

        self.page_label = tk.Label(
            self.controls_frame, bg=PRIMARY_BACKGROUND_COLOR, fg=TEXT_COLOR
        )
        self.page_label.grid(row=1, column=2)

        self.next_page_button = tk.Button(
            self.controls_frame, text=">", command=self.next_page
        )
        self.next_page_button.grid(row=1, column=3, padx=DEFAULT_PADDING)

        self.last_page_button = tk.Button(
            self.controls_frame, text=">>", command=self.last_page
        )
        self.last_page_button.grid(row=1, column=4)

        self.previous_next_buttons_state()

        # Content container
        self.content_container = tk.Frame(self.frame)
        self.content_container.pack(fill=tk.BOTH, expand=True, padx=DEFAULT_PADDING)

        self.show()

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()

    def set_collection(self, collection):
        """Set the actual collection"""
        if collection != self.collection:
            self.collection_page = 0
        self.collection = collection
        self.full_refresh()

    def first_page(self):
        """Go to the first page"""
        self.collection_page = 0
        self.previous_next_buttons_state()
        self.refresh()

    def previous_page(self):
        """Go to the previous page"""
        if self.collection_page > 0:
            self.collection_page -= 1

            self.previous_next_buttons_state()
            self.refresh()

    def next_page(self):
        """Go to the next page"""
        if self.collection_page + 1 < ceil(
            len(self.collection_content) / EXPLORER_MAX_BY_PAGE
        ):
            self.collection_page += 1

            self.previous_next_buttons_state()
            self.refresh()

    def last_page(self):
        """Go to the last page"""
        self.collection_page = max(
            0, ceil(len(self.collection_content) / EXPLORER_MAX_BY_PAGE) - 1
        )
        self.previous_next_buttons_state()
        self.refresh()

    def previous_next_buttons_state(self):
        """Enable or disable the previous and next buttons"""
        if self.collection_page == 0:
            self.previous_page_button.config(state=tk.DISABLED)
            self.first_page_button.config(state=tk.DISABLED)
        elif len(self.collection_content) / EXPLORER_MAX_BY_PAGE > 1:
            self.previous_page_button.config(state=tk.NORMAL)
            self.first_page_button.config(state=tk.NORMAL)
        if len(self.collection_content) / EXPLORER_MAX_BY_PAGE > 1:
            self.next_page_button.config(state=tk.NORMAL)
            self.last_page_button.config(state=tk.NORMAL)
        if self.collection_page + 1 >= ceil(
            len(self.collection_content) / EXPLORER_MAX_BY_PAGE
        ):
            self.next_page_button.config(state=tk.DISABLED)
            self.last_page_button.config(state=tk.DISABLED)

    def full_refresh(self):
        """Load collection content and refresh"""
        self.get_collection_content()
        self.refresh()

    def refresh(self):
        """Refresh the frame content"""
        self.load_collection_content()

        self.page_label.config(
            text=f"{self.collection_page + 1}/"
            f"{max(1, ceil(len(self.collection_content) / EXPLORER_MAX_BY_PAGE))}"
        )
        self.previous_next_buttons_state()

    def get_collection_content(self):
        """Get the collection content data"""
        self.collection_content = load(self.collection)
        self.collection_content.reverse()
        if self.collection_page + 1 > ceil(
            len(self.collection_content) / EXPLORER_MAX_BY_PAGE
        ):
            self.collection_page = ceil(
                len(self.collection_content) / EXPLORER_MAX_BY_PAGE
            )
            self.previous_next_buttons_state()

    def load_collection_content(self):
        """Display the collection content in the frame"""

        # Reset the cache
        self.content_cache = []

        # Delete actual content
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Empty element to reset size
        tk.Frame(self.content_container, width=0, height=0).pack()

        # Display the content
        for content_index in range(
            self.collection_page * EXPLORER_MAX_BY_PAGE,
            self.collection_page * EXPLORER_MAX_BY_PAGE + EXPLORER_MAX_BY_PAGE,
        ):
            if content_index >= len(self.collection_content):
                break

            saved_element = self.collection_content[content_index]

            if len(saved_element) == 2:
                saved_element_image_names = [
                    image_name for image_name in saved_element[0] if len(image_name) > 0
                ]

                saved_element_text = saved_element[1]

                self.content_cache.append(
                    ContentFrame(
                        self.content_container,
                        saved_element_image_names,
                        saved_element_text,
                        self.collection,
                        self.app.add_to_clipboard,
                    )
                )

        self.app.resize()


class ContentFrame:
    """A content container with a delete and edit button"""

    def __init__(self, parent, image_names, text, collection, add_clipboard_function):
        self.parent = parent
        self.image_names = image_names
        self.text = text
        self.collection = collection

        # Function to add content to the clipboard
        self.add_clipboard_function = add_clipboard_function

        self.image_cache = []

        # Create a container for the label and images
        self.frame = tk.Frame(
            self.parent,
            bg=SECONDARY_BACKGROUND_COLOR,
            borderwidth=2,
            relief="ridge",
            padx=DEFAULT_PADDING,
            pady=DEFAULT_PADDING,
        )

        # Display the text
        if len(self.text) > 0:
            copy_button = tk.Button(
                self.frame,
                text="Copy",
                command=lambda: add_clipboard_function(self.text),
            )
            copy_button.pack()

            text_label = tk.Label(
                self.frame, bg=SECONDARY_BACKGROUND_COLOR, fg=TEXT_COLOR, text=self.text
            )
            text_label.pack()

        # Display the images
        self.image_container = tk.Frame(
            self.frame,
            bg=SECONDARY_BACKGROUND_COLOR,
        )

        self.image_container.pack()

        # Index of the image in the list of images for grid placement
        index = 0

        for image_name in self.image_names:
            image_path = f"{SAVE_FOLDER}/{collection}/{image_name}{IMAGE_EXTENSION}"
            try:
                image = Image.open(image_path)
            except FileNotFoundError:
                continue

            # Resize the image with the size limit (keeping ratio)
            image_width = image.width
            image_height = image.height
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
            image_resized = image.resize((resize_width, resize_height), Image.ANTIALIAS)

            # Convert the image for Tkinter
            display_image = ImageTk.PhotoImage(image_resized)

            # Display the image
            self.create_button(display_image, image_path, index)
            self.image_cache.append(display_image)

            index += 1

        self.show()

    def create_button(self, image, path, index):
        """Create button to preview and open the image"""
        button_image = tk.Button(
            self.image_container, image=image, command=lambda: open_file(path)
        )
        button_image.grid(
            row=index // PREVIEW_IMAGES_BY_LINE + 1,
            column=index % PREVIEW_IMAGES_BY_LINE,
            padx=DEFAULT_PADDING,
            pady=DEFAULT_PADDING,
        )

    def show(self):
        """Show the image container"""
        self.frame.pack(pady=DEFAULT_PADDING)

    def hide(self):
        """Hide the image container"""
        self.frame.pack_forget()
