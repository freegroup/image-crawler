import os
import json
from PIL import Image

from configuration import Configuration
conf = Configuration()

class ReadFromFolderWorker():
    def __init__(self):
        self.__input = []
        self.__dir = conf.reader("dir")

        if not os.path.exists(self.__dir):
            print("WARNING: Input directory didn't exists")
            os.makedirs(self.__dir)

        # read all json files from the "read" directory and store them in an python list
        #
        candidates = [json for json in os.listdir(self.__dir) if json.endswith('.json')]
        for candidate in candidates:
            self.__input.append(candidate)

    def len(self):
        return len(self.__input)

    def read(self, index):
        json_file_name = os.path.join(self.__dir,self.__input[index])

        with open(json_file_name) as json_file:
            image_meta = json.load(json_file)
            path = json_file_name.replace("json", image_meta["format"].lower())
            image_meta["image"] = Image.open(path)
        return image_meta
