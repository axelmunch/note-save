""" Images and text saving """

from datetime import datetime

from .configuration import (
    IMAGE_EXTENSION,
    IMAGE_EXTENSION_TYPE,
    SAVE_FOLDER,
    TEXT_FILE_NAME,
    TEXT_IMAGE_SEPARATOR,
    TEXT_MARKER,
    TEXT_SEPARATOR,
)
from .files import create_full_path, is_file, is_folder


def get_time():
    """Return the current time in the format "YYYY-MM-DD_HH-MM-SS" """
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def name_image(folder, index=0):
    """Return a name for the image containing the
    current time and accounting for duplicates"""
    image_name = get_time()

    # If the folder already contains an image with the same name, increment it
    if is_file(
        f"{folder}/{image_name}{('_' + str(index)) * (index != 0)}"
        f"{IMAGE_EXTENSION}"
    ):
        return name_image(folder, index + 1)
    return f"{image_name}" + f"_{index}" * (index != 0)


def save(collection, text, images):
    """Save the text and images to the collection folder"""

    # Checking if the collection folder exists
    if not is_folder(f"{SAVE_FOLDER}/{collection}"):
        # If not, create it
        create_full_path(f"{SAVE_FOLDER}/{collection}")

    # Saving images with a custom name
    image_names = []
    for image in images:
        # Create a name
        image_name = name_image(f"{SAVE_FOLDER}/{collection}")
        image_names.append(image_name)
        # Save
        try:
            image.save(
                f"{SAVE_FOLDER}/{collection}/{image_name}{IMAGE_EXTENSION}",
                IMAGE_EXTENSION_TYPE,
            )
        except IOError as error:
            print(f"Cannot save image.\n{error}")
            return False

    # Saving text with a reference to the images
    text_to_save = (
        f"{TEXT_MARKER}{TEXT_IMAGE_SEPARATOR.join(image_names)}"
        f"{TEXT_SEPARATOR}{text}"
    )
    if text_to_save[-1] != "\n":
        text_to_save += "\n"
    try:
        add_text(f"{SAVE_FOLDER}/{collection}/{TEXT_FILE_NAME}", text_to_save)
    except FileNotFoundError as error:
        print(f"Cannot save text.\n{error}")
        return False

    return True


def add_text(file, text):
    """Append text to a file"""
    with open(file, "a", encoding="utf8") as opened_file:
        opened_file.write(text)
