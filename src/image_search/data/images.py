import pickle

class Images:

    def __init__(self, conf):
        self.__conf = conf
        print("done")
        # read the md5-hashes of all skipped images
        try:
            self.__skipped_images= pickle.load(open(self.__conf.imageDir+"/skipped_images.pickle", "rb"))
        except (OSError, IOError) as e:
            self.__skipped_images = []
            pickle.dump(self.__skipped_images, open(self.__conf.imageDir+"/skipped_images.pickle", "wb"))

        # read the md5-hashes of all valid images.
        # right now, the filename of the images must be the md5-hash