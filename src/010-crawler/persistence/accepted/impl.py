import os
import json
from threading import Thread
from PIL import Image

from configuration import Configuration
from persistence.hashes import MD5Inventory

conf = Configuration()
inventory = MD5Inventory()

class StoreToFolderWorker(Thread):
    def __init__(self, queue_input):
        Thread.__init__(self)
        self.setDaemon(True)
        self.__queue_input = queue_input
        self.__dir = conf.accepted("dir")

        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)

        json_files = [json for json in os.listdir(self.__dir) if json.endswith('.json')]
        for file in json_files:
            with open(os.path.join(self.__dir,file)) as json_file:
                data = json.load(json_file)
                inventory.add_already_accepted(data["md5"])
                inventory.add_already_accepted(data["url"])

    def run(self):
        "Calculate the MD5 hash of an image and store them with the has as filename"

        while True:
            try:
                image_meta = self.__queue_input.get()
                md5 = image_meta["md5"]
                url = image_meta["url"]
                img = image_meta["image"]
                format = img.format

                basewidth = int(conf.accepted("imagewidth"))
                wpercent = (basewidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((basewidth,hsize), Image.ANTIALIAS)

                img.save(os.path.join(self.__dir, md5 + "." + format.lower()))

                # save some meta data of the image side-by-side
                image_meta["format"] = format
                image_meta["width"] = img.size[0]
                image_meta["height"] = img.size[1]
                del image_meta["image"]
                json_data = json.dumps(image_meta, indent=4)
                with open(os.path.join(self.__dir, md5 + ".json"), "w") as f:
                    f.write(json_data)
                inventory.add_already_accepted(md5)
                inventory.add_already_accepted(url)

            except OSError:
                pass
