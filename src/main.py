#from sys import platform as sys_pf
#if sys_pf == 'darwin':
#    import matplotlib
#    matplotlib.use("TkAgg")

import queue
from pydoc import locate
from tkinter import Tk, Frame, StringVar, BOTH, ttk
from PIL import ImageTk, Image
from img_crawler.configuration import Configuration

queue_search_query = queue.Queue(maxsize=100)
queue_img_urls = queue.Queue(maxsize=100)
queue_img_fetched = queue.Queue(maxsize=100)
queue_img_appraised = queue.Queue(maxsize=100)
queue_img_accepted = queue.Queue(maxsize=1000)
queue_img_skipped = queue.Queue(maxsize=1000)

conf = Configuration(inifile="config.ini")

SearchWorker = locate(conf.impl_search())
search_worker = SearchWorker(queue_search_query, queue_img_urls)
search_worker.start()

ImageLoaderWorker = locate(conf.impl_loader())
loader_worker = ImageLoaderWorker(queue_img_urls, queue_img_fetched)
loader_worker.start()

ImageAppraiser = locate(conf.impl_appraiser())
accepted_worker = ImageAppraiser(queue_img_fetched, queue_img_appraised)
accepted_worker.start()

AcceptedImageWorker = locate(conf.impl_accepted())
accepted_worker = AcceptedImageWorker(queue_img_accepted)
accepted_worker.start()

SkippedImageWorker = locate(conf.impl_skipped())
skipped_worker = SkippedImageWorker(queue_img_skipped)
skipped_worker.start()


class Example(Frame):

    def __init__(self, root):
        super().__init__()
        self.__root = root
        self.search_term = StringVar()
        self.search_term.set(conf.ui(key="search_term"))

        self.initUI()

        self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.__root.lift()
        self.__root.attributes('-topmost', True)
        self.__root.after_idle(root.attributes, '-topmost', False)
        self.__root.mainloop()

    def initUI(self):
        self.__root.geometry("550x300+30+30")

        self.master.title("Image Search for Machine Learning")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = ttk.Entry(self, textvariable=self.search_term)
        lbl.grid(pady=4, padx=5, columnspan=4, sticky="EW")
        button_search = ttk.Button(self, text=conf.ui("search_text"), command=self.search_image)
        button_search.grid(row=0, column=4, sticky="EW")

        self.image_data = {"image": Image.open("blank.png") }
        img = ImageTk.PhotoImage(self.image_data["image"])
        self.image_preview = ttk.Label(self, image=img)
        self.image_preview.image = img
        self.image_preview.grid(row=1, column=0, columnspan=2, rowspan=6, sticky="EWSN")
        self.image_preview.bind('<Configure>', self._resize_image)

        skip_button = ttk.Button(self, text=conf.ui("skip_text"), command= self.skip_image_callback)
        skip_button.grid(row=7, column=0, sticky="WE")
        self.__root.bind(conf.ui("skip_hot_key"), self.skip_image_callback)

        keep_button = ttk.Button(self, text=conf.ui("keep_text"), command= self.keep_image_callback)
        keep_button.grid(row=7, column=1, sticky="WE")
        self.__root.bind(conf.ui("keep_hot_key"), self.keep_image_callback)


    def search_image(self):
        conf.search_term = self.search_term.get()
        queue_search_query.put(conf.search_term)

    def skip_image_callback(self, event=None):
        if 'md5' in self.image_data.keys():
            queue_img_skipped.put(self.image_data)
        self.display_next_image()

    def keep_image_callback(self, event=None):
        if 'md5' in self.image_data.keys():
            queue_img_accepted.put(self.image_data)
        self.display_next_image()

    def display_next_image(self):
        self.image_data = queue_img_appraised.get()

        new_width = self.image_preview.winfo_width()
        new_height = self.image_preview.winfo_height()

        img_copy = self.image_data["image"].copy()
        img_copy = img_copy.resize((new_width, new_height))
        img_copy = ImageTk.PhotoImage(img_copy)

        self.image_preview.image = img_copy
        self.image_preview.config(image=img_copy)

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height

        img_copy = self.image_data["image"].copy()
        img_copy = img_copy.resize((new_width, new_height))
        img_copy = ImageTk.PhotoImage(img_copy)
        self.image_preview.image = img_copy
        self.image_preview.config(image=img_copy)

    def on_closing(self):
        self.__root.destroy()


app = Example(Tk())
