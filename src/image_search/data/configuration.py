from configparser import ConfigParser



class Configuration:
    def __init__(self, conf_file):
        self.__file = conf_file
        self.__config = ConfigParser()
        self.__config.read(conf_file)

    @property
    def subscriptionKey(self):
        try:
            return self.__config['DEFAULT']['SUBSCRIPTION_KEY']
        except KeyError:
            return "no-key"

    @subscriptionKey.setter
    def subscriptionKey(self, val):
        self.__config['DEFAULT']['SUBSCRIPTION_KEY'] = val
        self.__dump()

    @property
    def imageDir(self):
        try:
            return self.__config['DEFAULT']['IMAGE_DIR']
        except KeyError:
            return "./data"

    @imageDir.setter
    def imageDir(self, val):
        self.__config['DEFAULT']['IMAGE_DIR'] = val
        self.__dump()

    @property
    def searchTerm(self):
        try:
            return self.__config['DEFAULT']['SEARCH_TERM']
        except KeyError:
            return "cat garden"

    @searchTerm.setter
    def searchTerm(self, val):
        self.__config['DEFAULT']['SEARCH_TERM'] = val
        self.__dump()

    def __dump(self):
        with open(self.__file, 'w') as f:
            self.__config.write(f)
