from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

import io
import requests
from PIL import Image
import matplotlib.pyplot as plt
from threading import Thread


class DownloadThread(Thread):
    def __init__(self, conf, queue_query, queue_result):
        Thread.__init__(self)
        self.__conf = conf
        self.__query = queue_query
        self.__result = queue_result

    def run(self):
        "Download images and forward them to the image queue"

        while True:
            try:
                img= self.__query.get()
                url = img["contentUrl"]
                data = requests.get(url).content
                img = Image.open(io.BytesIO(data))
                self.__result.put(img)
            except OSError:
                pass
