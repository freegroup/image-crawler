import os
import queue
from worker.download import DownloadThread
from worker.search import SearchThread
from data.configuration import Configuration
from data.images import Images

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image

queue_search_query = queue.Queue(maxsize=100)
queue_search_result = queue.Queue(maxsize=100)
queue_images = queue.Queue(maxsize=100)

conf = Configuration("config.ini")
images = Images(conf)

search = SearchThread(conf, queue_search_query, queue_search_result)
search.start()

downloader = DownloadThread(conf, queue_search_result, queue_images)
downloader.start()

dirpath = os.getcwd()

mypath = conf.image_dir
good = set([os.path.splitext(os.path.basename(f))[0] for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))])


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
        buttonBad = Button(self, text="Search", command=self.search_image)
        buttonBad.grid(row=0, column=4, sticky="EW")

        self.image = Image.open("blank.png")
        img = ImageTk.PhotoImage(self.image)
        self.imageLabel = ttk.Label(self, image=img)
        self.imageLabel.image = img
        self.imageLabel.grid(row=1, column=0, columnspan=2, rowspan=6, sticky="EWSN")
        self.imageLabel.bind('<Configure>', self._resize_image)

        lbl = Label(self, text="Image Directory")
        lbl.grid(row=1, column=3, pady=(20, 0),  sticky="W")
        entryBadPath = Entry(self, textvariable=self.image_dir)
        entryBadPath.grid(row=2, column=3)
        buttonBad = Button(self, text="Browse..", command=self.select_image_dir)
        buttonBad.grid(row=2, column=4)

        hbtn = Button(self, text="Skip Image")
        hbtn.grid(row=7, column=0, sticky="WE")
        root.bind("<Left>", self.bad_image_callback)

        obtn = Button(self, text="Keep Image")
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
        conf.imageDir = path
        self.image_dir.set(conf.imageDir)

    def search_image(self):
        conf.search_term = self.search_term.get()
        queue_search_query.put(conf.search_term)

    def bad_image_callback(self, event):
        print("bad image")

    def good_image_callback(self, event):
        print("good image")
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