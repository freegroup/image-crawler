import cv2
from skimage import transform
import os
import shutil

from configuration import Configuration
conf = Configuration()

class ExportToFolderWorker():
    def __init__(self):
        self.__dir = conf.exporter("dir")

        # cleanup and recreate the export directory
        if os.path.exists(self.__dir):
            shutil.rmtree(self.__dir)
        os.makedirs(self.__dir)

    def write(self, image_meta):
        labels = image_meta["labels"]
        img = image_meta["image"]

        for label in labels:
            id = label["id"]
            text = label["text"]
            x = label["x"]
            y = label["y"]
            width = label["width"]
            height = label["height"]
            # ensure that the directory for the "label" already exists
            label_path = os.path.join(self.__dir, text)
            if not os.path.exists(label_path):
                os.makedirs(label_path)

            # Convert any PNG/GIF to JPEG's for consistency.
            img.crop((x, y, x+width, y+height))\
                .convert('RGB')\
                .save(os.path.join(label_path, id + ".jpeg"), "JPEG")

    # just to provide a homogeneous interface
    def close(self):
        pass
