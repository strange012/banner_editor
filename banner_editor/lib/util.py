import os
import shutil
import string

from enum import Enum
from PIL import Image


def delete_contents(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


class PictureSize(Enum):
    list_icon = (144, 54)
    edit_image = (640, 240)
    rotator_banner = (1600, 600)


def image_resize(path, filename, size):
    image = Image.open(os.path.join(path, filename))
    image = image.resize(size.value, Image.NEAREST)
    image.save(os.path.join(path, size.name, filename))
