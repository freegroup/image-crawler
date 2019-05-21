import imagehash
from threading import Thread
from persistence.hashes import MD5Inventory

inventory = MD5Inventory()

class AvoidDuplicates(Thread):
    def __init__(self, queue_input, queue_output):
        Thread.__init__(self)
        self.setDaemon(True)
        self.__queue_input = queue_input
        self.__queue_output = queue_output


    def run(self):
        "Calculate the MD5 hash of an image and store them with the has as filename"

        while True:
            try:
                image_meta = self.__queue_input.get()
                if not inventory.has_hash(image_meta["md5"]):
                    self.__queue_output.put(image_meta)

            except OSError:
                pass

