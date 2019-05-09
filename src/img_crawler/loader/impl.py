#from sys import platform as sys_pf
#if sys_pf == 'darwin':
#    import matplotlib
#    matplotlib.use("TkAgg")

import io
import requests
import imagehash
from PIL import Image
from threading import Thread

from img_crawler.persistence.hashes import MD5Inventory

inventory = MD5Inventory()

# Fetches Images and stores them as PIL Image in the named queue
#
# queue_urls: must be a queue of strings. The strings must be valid URL's
# queue_images: The result of the downloaded images. pillow.Image
#
class URLDownloadWorker:

    def __init__(self, queue_input, queue_output):
        self.__queue_input = queue_input
        self.__queue_output = queue_output

    def start(self):
        URLDownloadWorker.__URLDownloadWorker(self.__queue_input, self.__queue_output).start()
        URLDownloadWorker.__URLDownloadWorker(self.__queue_input, self.__queue_output).start()
        URLDownloadWorker.__URLDownloadWorker(self.__queue_input, self.__queue_output).start()
        URLDownloadWorker.__URLDownloadWorker(self.__queue_input, self.__queue_output).start()
        URLDownloadWorker.__URLDownloadWorker(self.__queue_input, self.__queue_output).start()
        URLDownloadWorker.__URLDownloadWorker(self.__queue_input, self.__queue_output).start()

    class __URLDownloadWorker(Thread):
        def __init__(self, queue_input, queue_output):
            Thread.__init__(self)
            self.setDaemon(True)
            self.__queue_input = queue_input
            self.__queue_output = queue_output

        def run(self):
            "Download images and forward them to the image queue"

            while True:
                try:
                    meta_data = self.__queue_input.get()

                    # never load an image twice
                    url = meta_data["url"]
                    if not inventory.has_hash(url):
                        data = requests.get(url).content
                        img = Image.open(io.BytesIO(data))

                        # enrich the meta data with the image instance and the MD5 hash
                        meta_data["image"] = img
                        meta_data["md5"] = str(imagehash.dhash(img))

                        # forward to the next processors
                        self.__queue_output.put(meta_data)

                except OSError:
                    pass
