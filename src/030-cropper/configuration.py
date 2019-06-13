from configparser import ConfigParser


class Configuration:
    __config = None
    __file = None

    def __init__(self, inifile=None):
        if inifile is not None:
            Configuration.__file = inifile
            Configuration.__config = ConfigParser()
            Configuration.__config.read(Configuration.__file)


    def image_descriptor_by_type(self, ext):
        options = {
            "JPEG": "image/jpeg",
            "PNG": "image/png",
            "GIF": "image/gif"
        }
        return options.get(ext)

    def impl_reader(self):
        return self.reader(key='implementation', default="persistence.reader.impl.ReadFromFolderWorker")

    def impl_exporter(self):
        return self.exporter(key='implementation', default="persistence.exporter.impl.StoreToFolderWorker")

    def reader(self, key, val=None, default=None):
        return Configuration.getter_setter(section="READER", key=key, val=val, default=default)

    def exporter(self, key, val=None, default=None):
        return Configuration.getter_setter(section="EXPORTER", key=key, val=val, default=default)




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
