import imagehash
import os
import pickle
from threading import Thread


class AcceptImageWorker(Thread):
    def __init__(self, conf, queue):
        Thread.__init__(self)
        self.__conf = conf
        self.__queue = queue
        self.__dir = os.path.join(self.__conf.image_dir, "good")

        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)


    def run(self):
        "Calculate the MD5 hash of an image and store them with the has as filename"

        while True:
            try:
                img = self.__queue.get()
                hash = str(imagehash.dhash(img))
                img.save(os.path.join(self.__dir, hash+"."+img.format.lower()))
            except OSError:
                pass


class SkipImageWorker(Thread):
    def __init__(self, conf, queue):
        Thread.__init__(self)
        self.__conf = conf
        self.__queue = queue
        self.__dir = os.path.join(self.__conf.image_dir, "skipped")

        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)


    def run(self):
        "Calculate the MD5 hash of an image and store them with the has as filename"

        while True:
            try:
                img = self.__queue.get()
                hash = str(imagehash.dhash(img))
                img.save(os.path.join(self.__dir, hash+"."+img.format.lower()))
            except OSError:
                pass


class ImageIndexer(object):
    def __new__(cls, conf):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)

        cls.instance.__conf = conf
        # read the md5-hashes of all skipped images
        try:
            self.__skipped_images= pickle.load(open(self.__conf.image_dir+"/skipped/skipped_images.pickle", "rb"))
        except (OSError, IOError) as e:
            self.__skipped_images = []
            pickle.dump(self.__skipped_images, open(self.__conf.image_dir+"/skipped/skipped_images.pickle", "wb"))

        return cls.instance

