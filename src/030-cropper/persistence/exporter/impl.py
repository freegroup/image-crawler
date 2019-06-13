import os
import json

from configuration import Configuration
conf = Configuration()

class ExportToFolderWorker():
    def __init__(self):
        self.__dir = conf.exporter("dir")

        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)


    def write(self, image_meta):
        md5 = image_meta["md5"]
        img = image_meta["image"]
        del image_meta["image"]

        img.save(os.path.join(self.__dir, md5 + "." + img.format.lower()))
        json_data = json.dumps(image_meta, indent=4)
        with open(os.path.join(self.__dir, md5 + ".json"), "w") as f:
            f.write(json_data)

