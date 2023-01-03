"""Loading texts and image names from a collection"""

from .configuration import (
    SAVE_FOLDER,
    TEXT_FILE_NAME,
    TEXT_IMAGE_SEPARATOR,
    TEXT_MARKER,
    TEXT_SEPARATOR,
)


def read_text(file):
    """Read text from a file"""
    try:
        with open(file, "r", encoding="utf8") as opened_file:
            return opened_file.read()
    except FileNotFoundError:
        return ""


def load(collection):
    """Load a collection as a list of file names and texts"""
    text_content = read_text(f"{SAVE_FOLDER}/{collection}/{TEXT_FILE_NAME}")

    entries = text_content.split(sep=TEXT_MARKER)
    del entries[0]

    # list[tuple[list[str], str]] [(file names, text) ...]
    elements = []

    for entry in entries:
        splitted_entry = entry.split(sep=TEXT_SEPARATOR)
        image_names = splitted_entry[0].split(sep=TEXT_IMAGE_SEPARATOR)
        if len(splitted_entry) > 1:
            text = splitted_entry[1:]
            if len(text) > 0 and text[-1] == "":
                del text[-1]
            # Joining the rest if the separator is in the text
            text = TEXT_SEPARATOR.join(text)
        else:
            text = ""

        elements.append((image_names, text))

    return elements
