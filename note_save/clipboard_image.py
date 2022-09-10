from PIL import Image, ImageGrab


def get_clipboard():
    # Image, list of file names or None
    return ImageGrab.grabclipboard()

def load_image(path):
    # Return the opened Image or None
    try:
        return Image.open(path)
    except:
        return None

def get_clipboard_images():
    images = []

    clipboard_content = get_clipboard()
    if isinstance(clipboard_content, Image.Image):
        # Is a single image
        images.append(clipboard_content)
    
    elif isinstance(clipboard_content, list):
        # Is a list of paths
        for path in clipboard_content:
            data = load_image(path)
            if data != None:
                # The data is an image
                images.append(data)

    return images