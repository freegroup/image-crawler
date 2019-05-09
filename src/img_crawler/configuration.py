from configparser import ConfigParser


class Configuration:
    __config = None
    __file = None

    def __init__(self, inifile=None):
        if inifile is not None:
            Configuration.__file = inifile
            Configuration.__config = ConfigParser()
            Configuration.__config.read(Configuration.__file)

    def impl_search(self):
        return self.search(key='implementation', default="img_crawler.search.impl.BingSearchWorker")

    def impl_loader(self):
        return self.loader(key='implementation', default="img_crawler.loader.impl.URLDownloadWorker")

    def impl_accepted(self):
        return self.accepted(key='implementation', default="img_crawler.persistence.accepted.impl.StoreToFolderWorker")

    def impl_skipped(self):
        return self.skipped(key='implementation', default="img_crawler.persistence.skipped.impl.StoreToFolderWorker")

    def impl_appraiser(self):
        return self.appraiser(key='implementation', default="img_crawler.appraiser.impl.AvoidDuplicates")

    def appraiser(self, key, val=None, default=None):
        return Configuration.getter_setter(section="appraiser", key=key, val=val, default=default)

    def ui(self, key, val=None, default=None):
        return Configuration.getter_setter(section="UI", key=key, val=val, default=default)

    def accepted(self, key, val=None, default=None):
        return Configuration.getter_setter(section="ACCEPTED", key=key, val=val, default=default)

    def skipped(self, key, val=None, default=None):
        return Configuration.getter_setter(section="SKIPPED", key=key, val=val, default=default)

    def loader(self, key, val=None, default=None):
        return Configuration.getter_setter(section="LOADER", key=key, val=val, default=default)

    def search(self, key, val=None, default=None):
        return Configuration.getter_setter(section="SEARCH", key=key, val=val, default=default)



    @staticmethod
    def getter_setter(section, key, val, default):
        if val is None:
            try:
                return Configuration.__config[section][key]
            except KeyError:
                return default

        Configuration.__config[section][key] = val
        with open(Configuration.__file, 'w') as f:
            Configuration.__config.write(f)
