from configuration import *
from files import *
from datetime import datetime


def get_time():
    # Return the current time in the format "YYYY-MM-DD_HH-MM-SS"

    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def name_image(folder, index = 0):
    # Return a name for the image containing the current time accounting for duplicates

    # Generate a name for the image based on the time
    image_name = get_time()

    # If the folder contains an image with the same name, increment the name
    if is_file(f"{folder}/{image_name}{('_' + str(index)) * (index != 0)}{IMAGE_EXTENSION}"):
        return name_image(folder, index + 1)
    else:
        return f"{image_name}" + f"_{index}" * (index != 0)

def save(collection, text, images):
    # Save the text and images to the collection folder

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
        image.save(f"{SAVE_FOLDER}/{collection}/{image_name}{IMAGE_EXTENSION}", IMAGE_EXTENSION_TYPE)

    # Saving text with a reference to the images
    add_text(f"{SAVE_FOLDER}/{collection}/{TEXT_FILE_NAME}", f"{TEXT_MARKER}{TEXT_IMAGE_SEPARATOR.join(image_names)}{TEXT_SEPARATOR}{text}")

def add_text(file, text):
    # Add text to a file

    with open(file, 'a', encoding = "utf8") as f:
        f.write(text)