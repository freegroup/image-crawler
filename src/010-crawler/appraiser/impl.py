import imagehash
from threading import Thread
from persistence.hashes import MD5Inventory
from configuration import Configuration

inventory = MD5Inventory()
conf = Configuration()

class ValidateLoadedImages(Thread):
    def __init__(self, queue_input, queue_good, queue_bad):
        Thread.__init__(self)
        self.setDaemon(True)
        self.__queue_input = queue_input
        self.__queue_good = queue_good
        self.__queue_bad = queue_bad


    def run(self):
        "Calculate the MD5 hash of an image and store them with the has as filename"

        while True:
            try:
                image_meta = self.__queue_input.get()

                # avoid duplicate
                if not inventory.has_hash(image_meta["md5"]):
                    # avoid unsupported image format
                    img = image_meta["image"]
                    if conf.image_descriptor_by_type(img.format) is not None:
                        self.__queue_good.put(image_meta)
                    else:
                        # store unsupported files to avoid duplicate loading
                        self.__queue_bad.put(image_meta)

            except OSError:
              pass
