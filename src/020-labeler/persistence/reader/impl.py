import os
import json
from PIL import Image

from configuration import Configuration
conf = Configuration()

class ReadFromFolderWorker():
    def __init__(self, queue_candidates):
        self.__input = queue_candidates
        self.__reader_dir = conf.reader("dir")
        self.__exporter_dir = conf.exporter("dir")

        if not os.path.exists(self.__reader_dir):
            os.makedirs(self.__reader_dir)

        # read all json files from the "read" directory and store them in an python list
        #
        candidates = [json for json in os.listdir(self.__reader_dir) if json.endswith('.json')]
        for candidate in candidates:
            self.__input.append(candidate)

    def read(self, index):
        # try to load the already generated labeled version of the meta data
        json_file_name = os.path.join(self.__exporter_dir, self.__input[index])
        if not os.path.isfile(json_file_name):
            json_file_name = os.path.join(self.__reader_dir,self.__input[index])

        with open(json_file_name) as json_file:
            image_meta = json.load(json_file)
            if 'labels' not in image_meta.keys():
                image_meta["labels"] = []
            path = json_file_name.replace("json", image_meta["format"].lower())
            image_meta["image"] = Image.open(path)
        return image_meta
