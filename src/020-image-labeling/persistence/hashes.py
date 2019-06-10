

class MD5Inventory:
    __exported = []

    def __init__(self):
        pass

    def count_already_exported(self):
        return len(MD5Inventory.__exported)

    def add_already_exported(self, md5):
        if isinstance(md5, list):
            MD5Inventory.__exported.extend(md5)
        elif isinstance(md5, str):
            MD5Inventory.__exported.append(md5)

    def has_hash(self, md5):
        return (md5 in MD5Inventory.__exported)

