from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

import queue
from worker.download import DownloadWorker
from worker.search import SearchWorker
from worker.image import AcceptImageWorker, SkipImageWorker, ImageIndexer

from configuration import Configuration

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

queue_search_query = queue.Queue(maxsize=100)
queue_search_result = queue.Queue(maxsize=100)
queue_images = queue.Queue(maxsize=100)
queue_accept = queue.Queue(maxsize=1000)
queue_skip = queue.Queue(maxsize=1000)

conf = Configuration("config.ini")
image_indexer = ImageIndexer(conf)
image_indexer.start()

search_worker = SearchWorker(conf, queue_search_query, queue_search_result)
search_worker.start()

download_worker = DownloadWorker(conf, queue_search_result, queue_images)
download_worker.start()

accept_worker = AcceptImageWorker(conf, queue_accept)
accept_worker.start()

skip_worker = SkipImageWorker(conf, queue_skip)
skip_worker.start()


root = Tk()

class Example(Frame):

    def __init__(self):
        super().__init__()
        self.image_dir = StringVar()
        self.image_dir.set(conf.image_dir)

        self.search_term = StringVar()
        self.search_term.set(conf.search_term)

        self.initUI()

    def initUI(self):
        self.master.title("Image Search for Machine Learning")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = Entry(self, textvariable=self.search_term)
        lbl.grid(pady=4, padx=5, columnspan=4, sticky="EW")
        buttonBad = ttk.Button(self, text="Search", command=self.search_image)
        buttonBad.grid(row=0, column=4, sticky="EW")

        self.image = Image.open("blank.png")
        img = ImageTk.PhotoImage(self.image)
        self.imageLabel = ttk.Label(self, image=img)
        self.imageLabel.image = img
        self.imageLabel.grid(row=1, column=0, columnspan=2, rowspan=6, sticky="EWSN")
        self.imageLabel.bind('<Configure>', self._resize_image)

        lbl = ttk.Label(self, text="Image Directory")
        lbl.grid(row=1, column=3, pady=(20, 0),  sticky="W")
        entryBadPath = ttk.Entry(self, textvariable=self.image_dir)
        entryBadPath.grid(row=2, column=3)
        buttonBad = ttk.Button(self, text="Browse..", command=self.select_image_dir)
        buttonBad.grid(row=2, column=4)

        hbtn = ttk.Button(self, text="Skip Image")
        hbtn.grid(row=7, column=0, sticky="WE")
        root.bind("<Left>", self.bad_image_callback)

        obtn = ttk.Button(self, text="Keep Image")
        obtn.grid(row=7, column=1, sticky="WE")
        root.bind("<Right>", self.good_image_callback)

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        img_copy= self.image.copy()
        img_copy = img_copy.resize((new_width, new_height))
        img_copy = ImageTk.PhotoImage(img_copy)
        self.imageLabel.image=img_copy
        self.imageLabel.config(image=img_copy)

    def select_image_dir(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        path = filedialog.askdirectory().replace(dirpath, ".")
        print(path)
        conf.image_dir = path
        self.image_dir.set(conf.image_dir)

    def search_image(self):
        conf.search_term = self.search_term.get()
        queue_search_query.put(conf.search_term)

    def bad_image_callback(self, event):
        print("bad image")
        queue_skip.put(self.image)
        self.display_next_image()

    def good_image_callback(self, event):
        print("good image")
        queue_accept.put(self.image)
        self.display_next_image()

    def display_next_image(self):
        self.image= queue_images.get()

        new_width = self.imageLabel.winfo_width()
        new_height = self.imageLabel.winfo_height()

        img_copy= self.image.copy()
        img_copy = img_copy.resize((new_width, new_height))
        img_copy = ImageTk.PhotoImage(img_copy)

        self.imageLabel.image=img_copy
        self.imageLabel.config(image=img_copy)


def main():
    root.geometry("550x300+30+30")
    app = Example()
    root.lift()
    root.attributes('-topmost',True)
    root.after_idle(root.attributes,'-topmost',False)
    root.mainloop()


if __name__ == '__main__':
    main()