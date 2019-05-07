from configparser import ConfigParser



class Configuration:
    def __init__(self, conf_file):
        self.__file = conf_file
        self.__config = ConfigParser()
        self.__config.read(conf_file)

    @property
    def subscription_key(self):
        try:
            return self.__config['DEFAULT']['SUBSCRIPTION_KEY']
        except KeyError:
            return "no-key"

    @subscription_key.setter
    def subscription_key(self, val):
        self.__config['DEFAULT']['SUBSCRIPTION_KEY'] = val
        self.__dump()

    @property
    def image_dir(self):
        try:
            return self.__config['DEFAULT']['IMAGE_DIR']
        except KeyError:
            return "./data"

    @image_dir.setter
    def image_dir(self, val):
        self.__config['DEFAULT']['IMAGE_DIR'] = val
        self.__dump()

    @property
    def search_term(self):
        try:
            return self.__config['DEFAULT']['SEARCH_TERM']
        except KeyError:
            return "cat garden"

    @search_term.setter
    def search_term(self, val):
        self.__config['DEFAULT']['SEARCH_TERM'] = val
        self.__dump()

    def __dump(self):
        with open(self.__file, 'w') as f:
            self.__config.write(f)
