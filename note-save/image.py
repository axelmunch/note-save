from PIL import Image, ImageGrab


def get_clipboard():
    # Image, list of filenames or None
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
        return [clipboard_content]
    
    if isinstance(clipboard_content, list):
        for path in clipboard_content:
            data = load_image(path)
            if data != None:
                # The data is an image
                images.append(data)

    return images