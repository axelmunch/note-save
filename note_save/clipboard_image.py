"""Getting images from the clipboard"""

from PIL import Image, ImageGrab


def get_clipboard():
    """Return an image, a list of file names or None"""
    try:
        return ImageGrab.grabclipboard()
    except OSError:
        return None


def load_image(path):
    """Return the opened Image or None"""
    try:
        return Image.open(path)
    except (Image.UnidentifiedImageError, FileNotFoundError):
        return None


def get_clipboard_images():
    """Return a list of images from the clipboard"""
    images = []

    clipboard_content = get_clipboard()
    if clipboard_content is None:
        return images
    if isinstance(clipboard_content, Image.Image):
        # Is a single image
        images.append(clipboard_content)

    elif isinstance(clipboard_content, list):
        # Is a list of paths
        for path in clipboard_content:
            data = load_image(path)
            if data is not None:
                # The data is an image
                images.append(data)

    return images
