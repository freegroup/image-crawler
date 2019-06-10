import os
import json
from threading import Thread
from PIL import Image

from configuration import Configuration
from persistence.hashes import MD5Inventory

conf = Configuration()
inventory = MD5Inventory()

class ReadFromFolderWorker(Thread):
    def __init__(self, queue_candidates, queue_loaded):
        Thread.__init__(self)
        self.setDaemon(True)
        self.__queue_input = queue_candidates
        self.__queue_output = queue_loaded
        self.__dir = conf.reader("dir")

        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)

        # read the images and add the
        self.json_files = [json for json in os.listdir(self.__dir) if json.endswith('.json')]
        print(len(self.json_files))
        for file in self.json_files:
            print(file)
            with open(os.path.join(self.__dir,file)) as json_file:
                data = json.load(json_file)
                if not inventory.has_hash(data["md5"]):
                    self.__queue_input.put(data)

    def run(self):

        while True:
            try:
                image_meta = self.__queue_input.get()
                md5 = image_meta["md5"]
                path = os.path.join(self.__dir,md5)
                image = None
                if os.path.isfile(path+".jpeg"):
                    image = Image.open(path+".jpeg")
                elif os.path.isfile(path+".png"):
                    image = Image.open(path+".png")
                image_meta["image"] = image

                self.__queue_output.put(image_meta)

            except OSError:
                pass


