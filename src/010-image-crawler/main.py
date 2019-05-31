#from sys import platform as sys_pf
#if sys_pf == 'darwin':
#    import matplotlib
#    matplotlib.use("TkAgg")

import queue

from pydoc import locate
from tkinter import Tk, Frame, StringVar, BOTH, ttk, DISABLED
from PIL import ImageTk, Image, ImageOps
from configuration import Configuration
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# Load the app configuration
#
conf = Configuration(inifile=os.path.join(dir_path,"..", "config.ini"))

# Some sync. queue to handle the differnet threads for searching, loading, grouping,...
#
queue_search_query = queue.Queue(maxsize=100)
queue_img_urls = queue.Queue(maxsize=100)
queue_img_fetched = queue.Queue(maxsize=100)
queue_img_appraised = queue.Queue(maxsize=100)
queue_img_accepted = queue.Queue(maxsize=1000)
queue_img_skipped = queue.Queue(maxsize=1000)

# Init the configured Worker for Searching, Appraising,...
# You can easy implement your very own "GoogleSearcher" instead of the BingSearcher.
# Even searching images from a local directory is possible
#
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


# Very basic UI for the image search and selection.
#
class App(Frame):

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
        style = ttk.Style()
        style.map("C.TButton",
                  foreground=[
                      ('disabled', 'grey')
                  ],
                  background=[

                  ]
                  )

        self.master.title("Image Search for Machine Learning")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = ttk.Entry(self, textvariable=self.search_term)
        lbl.grid(pady=4, padx=5, columnspan=4, sticky="EW")
        button_search = ttk.Button(self, text=conf.ui("search_text"), command=self.search_image, style="C.TButton")
        button_search.grid(row=0, column=4, sticky="EW")

        self.image_blank = {"image": Image.open(os.path.join(dir_path,"blank.png")) }
        self.image_loading= {"image": Image.open(os.path.join(dir_path,"loading.png")) }
        self.image_current = self.image_blank

        img = ImageTk.PhotoImage(self.image_current["image"])
        self.image_preview = ttk.Label(self, image=img, anchor='center')
        self.image_preview.image = img
        self.image_preview.grid(row=1, column=0, columnspan=2, rowspan=6, sticky='EW')
        self.image_preview.bind('<Configure>', self._resize_image)

        self.skip_button = ttk.Button(self, text=conf.ui("skip_text"), command= self.skip_image_callback, style="C.TButton")
        self.skip_button.grid(row=7, column=0, sticky="WE")
        self.skip_button.state(["disabled"])   # Disable the button.
        self.__root.bind(conf.ui("skip_hot_key"), self.skip_image_callback)

        self.keep_button = ttk.Button(self, text=conf.ui("keep_text"), command= self.keep_image_callback, style="C.TButton")
        self.keep_button.grid(row=7, column=1, sticky="WE")
        self.keep_button.config(state=DISABLED)  # Enable the button.
        self.__root.bind(conf.ui("keep_hot_key"), self.keep_image_callback)
        self.after(1000, self.check_for_image)


    # Called if the user pressed the "search" button. Now the current active search term is posted
    # to the "queue_search_query" queue. The "search" thread picks up the new search term and starts crawling
    # images related to the new search term
    #
    def search_image(self):
        conf.search_term = self.search_term.get()
        queue_search_query.put(conf.search_term)
        try:
            while True:
                queue_img_urls.get_nowait()
        except queue.Empty:
            pass
        try:
            while True:
                queue_img_fetched.get_nowait()
        except queue.Empty:
            pass
        self.display_next_image()

    # Called of the user press the button or the configured key for "skipping" an image.
    # The method moves the current display image into the "skipped" queue.
    # The worker thread picks up this image and moves them into the related folder
    #
    def skip_image_callback(self, event=None):
        if 'md5' in self.image_current.keys():
            queue_img_skipped.put(self.image_current)
        self.display_next_image()

    # Called of the user press the button or the configured key for "keep" an image.
    # The method moves the current display image into the "keep" queue.
    # The worker thread picks up this image and moves them into the related folder
    #
    def keep_image_callback(self, event=None):
        if 'md5' in self.image_current.keys():
            queue_img_accepted.put(self.image_current)
        self.display_next_image()

    def check_for_image(self):
        print("check")
        if queue_img_appraised.qsize()>0 and self.image_current == self.image_loading :
            self.display_next_image()
        self.after(1000, self.check_for_image)


# Load the next image from the queue and display them in the UI
    #
    def display_next_image(self):
        if queue_img_appraised.qsize()>0  :
            self.image_current = queue_img_appraised.get()
            self.skip_button.state(["!disabled"])   # Disable the button.
            self.keep_button.state(["!disabled"])  # Enable the button.
        else:
            self.image_current = self.image_loading
            self.skip_button.state(["disabled"])   # Disable the button.
            self.keep_button.state(["disabled"])  # Enable the button.


        new_width = self.image_preview.winfo_width()
        new_height = self.image_preview.winfo_height()

        img_copy = self.image_current["image"].copy()
        img_copy = img_copy.resize((new_width, new_height))
        img_copy = ImageTk.PhotoImage(img_copy)

        self.image_preview.image = img_copy
        self.image_preview.config(image=img_copy)
        self._resize_image(None)

    def _resize_image(self, event):
        new_width = self.image_preview.winfo_width()
        new_height = self.image_preview.winfo_height()


        img_copy = self.image_current["image"].copy()
        img_copy = ImageOps.fit(img_copy, (min(new_width, new_height),min(new_width, new_height)), Image.ANTIALIAS)

        img_copy = ImageTk.PhotoImage(img_copy)
        self.image_preview.image = img_copy
        self.image_preview.config(image=img_copy)

    def on_closing(self):
        self.__root.destroy()


app = App(Tk())
