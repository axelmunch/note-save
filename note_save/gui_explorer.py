"""Explorer GUI"""

import tkinter as tk
from math import ceil
from threading import Thread
from tkinter import TclError

from PIL import Image, ImageTk

from .configuration import (
    DEFAULT_PADDING,
    EXPLORER_MAX_LINES_BY_PAGE,
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
        self.pages_media_length = []

        self.content_cache = []

        self.reverse = tk.IntVar()

        self.showing = False

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

        # Reverse checkbox
        self.reverse_checkbutton = tk.Checkbutton(
            self.controls_frame,
            text="Reverse",
            variable=self.reverse,
            command=self.event_reverse,
        )
        self.reverse_checkbutton.grid(row=1, column=5, padx=DEFAULT_PADDING)

        # Content container
        self.content_container = tk.Frame(self.frame)
        self.content_container.pack(fill=tk.BOTH, expand=True)

        self.show()

    def show(self):
        self.showing = True
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.showing = False
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
        if self.collection_page + 1 < self.page_count():
            self.collection_page += 1

            self.previous_next_buttons_state()
            self.refresh()

    def last_page(self):
        """Go to the last page"""
        self.collection_page = self.page_count() - 1

        self.previous_next_buttons_state()
        self.refresh()

    def previous_next_buttons_state(self):
        """Enable or disable the previous and next buttons"""
        if self.collection_page > 0:
            self.previous_page_button.config(state=tk.NORMAL)
            self.first_page_button.config(state=tk.NORMAL)
        else:
            self.previous_page_button.config(state=tk.DISABLED)
            self.first_page_button.config(state=tk.DISABLED)

        if self.collection_page + 1 < self.page_count():
            self.next_page_button.config(state=tk.NORMAL)
            self.last_page_button.config(state=tk.NORMAL)
        else:
            self.next_page_button.config(state=tk.DISABLED)
            self.last_page_button.config(state=tk.DISABLED)

    def get_pages_media_number(self):
        """Get the number of medias for each page and line"""
        self.pages_media_length = []
        page = []
        lines_in_page = 0
        lines = []
        line = []

        # list[tuple[list[str], str]] [(file names, text) ...]
        for content in self.collection_content:
            # Get the number of medias in the content, 1 by default for the text
            media_length = max(1, len(content[0]))

            if sum(line) + media_length <= PREVIEW_IMAGES_BY_LINE:
                # The media length can be added to the page
                line.append(media_length)
            else:
                # The line is full, add it to the list
                lines.append(line)
                line = [media_length]

        # Add the rest
        if len(line) > 0:
            lines.append(line)

        for line in lines:
            # If line contains more than PREVIEW_IMAGES_BY_LINE medias, it will take multiple lines
            line_and_overflow = ceil(sum(line) / PREVIEW_IMAGES_BY_LINE)

            if lines_in_page + line_and_overflow <= EXPLORER_MAX_LINES_BY_PAGE:
                # The line can be added to the page
                page.append(line)
                lines_in_page += line_and_overflow
            else:
                # The page is full, add it to the list
                self.pages_media_length.append(page)
                page = [line]
                lines_in_page = line_and_overflow

        # Add the rest
        if len(page) > 0:
            self.pages_media_length.append(page)

    def page_count(self):
        """Get the number of pages"""
        return len(self.pages_media_length)

    def event_reverse(self, event=None):
        """Reverse the collection"""
        del event
        self.full_refresh()

    def full_refresh(self):
        """Load collection content and refresh"""
        if self.showing:
            self.get_collection_content()
            self.refresh()

    def refresh(self):
        """Refresh the frame content"""
        self.display_collection_content()

        self.page_label.config(
            text=f"{self.collection_page + 1}/" f"{max(1, self.page_count())}"
        )
        self.previous_next_buttons_state()

    def get_collection_content(self):
        """Get the collection content data"""
        self.collection_content = load(self.collection)
        if not self.reverse.get():
            self.collection_content.reverse()
        self.get_pages_media_number()
        if self.collection_page + 1 > self.page_count():
            self.collection_page = self.page_count() - 1
            self.previous_next_buttons_state()

    def display_collection_content(self):
        """Display the collection content in the frame"""

        # Reset the cache
        self.content_cache = []

        # Delete actual content
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Empty element to reset size
        tk.Frame(self.content_container, width=0, height=0).pack()

        # Find the index of the first element in the page
        starting_index = 0
        for page_index in range(0, self.collection_page):
            starting_index += sum([len(l) for l in self.pages_media_length[page_index]])

        # Display the content
        if len(self.collection_content) > 0:
            for content_index in range(
                starting_index,
                starting_index
                + sum([len(l) for l in self.pages_media_length[self.collection_page]]),
            ):
                grid_x = None
                # grid_y = None
                columns = None

                # Find the location on the grid with the index
                index_in_grid = 0
                for line in range(len(self.pages_media_length[self.collection_page])):
                    for column in range(
                        len(self.pages_media_length[self.collection_page][line])
                    ):
                        if index_in_grid == content_index - starting_index:
                            columns = self.pages_media_length[self.collection_page][
                                line
                            ][column]
                            grid_x = column
                            # grid_y = line
                        index_in_grid += 1

                saved_element = self.collection_content[content_index]

                if len(saved_element) == 2:
                    # Names of the images
                    saved_element_image_names = [
                        image_name
                        for image_name in saved_element[0]
                        if len(image_name) > 0
                    ]

                    # Text
                    saved_element_text = saved_element[1]

                    # Grid display as Frame (pack) containing ContentFrame (grid)
                    if grid_x == 0:
                        # New line
                        self.content_cache.append(tk.Frame(self.content_container))
                        self.content_cache[-1].pack()

                    self.content_cache.insert(
                        0,
                        ContentFrame(
                            self.content_cache[-1],
                            saved_element_image_names,
                            saved_element_text,
                            self.collection,
                            self.app.add_to_clipboard,
                            grid_x,
                            0,
                            columns,
                        ),
                    )

        self.app.resize()


class ContentFrame:
    """A content container"""

    def __init__(
        self,
        parent,
        image_names,
        text,
        collection,
        add_clipboard_function,
        grid_x,
        grid_y,
        columns,
    ):
        self.parent = parent
        self.image_names = image_names
        self.text = text
        self.collection = collection

        # Function to add content to the clipboard
        self.add_clipboard_function = add_clipboard_function

        # Grid position
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.columns = columns

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
                self.frame,
                bg=SECONDARY_BACKGROUND_COLOR,
                fg=TEXT_COLOR,
                text=self.text,
                wraplength=MAX_PREVIEW_IMAGE_SIZE * self.columns,
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
            # self.load_image(image_path, index)
            Thread(target=self.load_image, args=(image_path, index)).start()

            index += 1

        self.show()

    def load_image(self, image_path, index):
        """Load an image in the frame"""
        try:
            image = Image.open(image_path)
        except FileNotFoundError:
            return

        # Resize the image with the size limit (keeping ratio)
        image_width = image.width
        image_height = image.height
        if image_width > image_height:
            resize_width = MAX_PREVIEW_IMAGE_SIZE
            resize_height = int(image_height / (image_width / MAX_PREVIEW_IMAGE_SIZE))
        else:
            resize_height = MAX_PREVIEW_IMAGE_SIZE
            resize_width = int(image_width / (image_height / MAX_PREVIEW_IMAGE_SIZE))
        image_resized = image.resize((resize_width, resize_height), Image.ANTIALIAS)

        # Convert the image for Tkinter
        display_image = ImageTk.PhotoImage(image_resized)

        # Display the image
        try:
            self.create_open_button(display_image, image_path, index)
        except TclError:
            return
        self.image_cache.append(display_image)

    def create_open_button(self, image, path, index):
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
        self.frame.grid(
            padx=DEFAULT_PADDING,
            pady=DEFAULT_PADDING,
            row=self.grid_y,
            column=self.grid_x,
        )

    def hide(self):
        """Hide the image container"""
        self.frame.grid_forget()
