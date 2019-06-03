

class MD5Inventory:
    __accepted = []
    __skipped = []

    def __init__(self):
        pass

    def count_already_accepted(self):
        return len(MD5Inventory.__accepted)/2

    def add_already_accepted(self, md5):
        if isinstance(md5, list):
            MD5Inventory.__accepted.extend(md5)
        elif isinstance(md5, str):
            MD5Inventory.__accepted.append(md5)

    def add_already_skipped(self, md5):
        if isinstance(md5, list):
            MD5Inventory.__skipped.extend(md5)
        elif isinstance(md5, str):
            MD5Inventory.__skipped.append(md5)

    def has_hash(self, md5):
        return (md5 in MD5Inventory.__skipped) or (md5 in MD5Inventory.__accepted)

