import os
import json

from configuration import Configuration
from persistence.hashes import MD5Inventory

conf = Configuration()
inventory = MD5Inventory()

class ReadFromFolderWorker():
    def __init__(self, queue_candidates):
        self.__input = queue_candidates
        self.__dir = conf.reader("dir")

        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)


    def start(self):
        # read the images and add the
        candidates = [os.path.join(self.__dir,json) for json in os.listdir(self.__dir) if json.endswith('.json')]
        for candidate in candidates:
            with open(candidate) as json_file:
                data = json.load(json_file)
                if not inventory.has_hash(data["md5"]):
                    self.__input.append(candidate)
