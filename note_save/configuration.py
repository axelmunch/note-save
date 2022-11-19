""" Configuration constants """

VERSION = "1.4"

SAVE_FOLDER = "saved"
DEFAULT_COLLECTION_NAME = "Default"

DEFAULT_PADDING = 10

TEXT_LINE_HEIGHT = 5

IMAGE_EXTENSION = ".png"
IMAGE_EXTENSION_TYPE = "PNG"

TEXT_FILE_NAME = "TEXTS.txt"

# Between each entry
TEXT_MARKER = "\x1f<§█ Entry █§>"
# Between image names
TEXT_IMAGE_SEPARATOR = ", "
# Between images and text
TEXT_SEPARATOR = "\n"


BANNER_BACKGROUND_COLOR = "#888888"
PRIMARY_BACKGROUND_COLOR = "#F0F0F0"
SECONDARY_BACKGROUND_COLOR = "#FFFFFF"
TEXT_COLOR = "#000000"

MAX_PREVIEW_IMAGE_SIZE = 200

VALID_FILE_NAME_CHARACTERS = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_ "
)
VALID_FILE_NAME_PATTERN = "[a-zA-Z0-9-_ ]+"
