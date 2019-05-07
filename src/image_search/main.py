import os
from worker.search import SearchThread
from data.configuration import Configuration
from data.images import Images

from tkinter import *
from tkinter import filedialog

conf = Configuration("config.ini")
images = Images(conf)

dirpath = os.getcwd()

mypath = conf.imageDir
good = set([os.path.splitext(os.path.basename(f))[0] for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))])


root = Tk()

class Example(Frame):

    def __init__(self):
        super().__init__()
        self.image_dir = StringVar()
        self.image_dir.set(conf.imageDir)

        self.search_term = StringVar()
        self.search_term.set(conf.searchTerm)

        self.initUI()
        self.search = SearchThread(10)
        self.search.start()

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

        area = Text(self)
        area.grid(row=1, column=0, columnspan=2, rowspan=6,
                  padx=5, sticky="EWSN")

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

    def select_image_dir(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        path = filedialog.askdirectory().replace(dirpath, ".")
        conf.imageDir = path
        self.image_dir.set(conf.imageDir)

    def search_image(selfself):
        print("search")

    @staticmethod
    def bad_image_callback(event):
        print("bad image")

    @staticmethod
    def good_image_callback(event):
        print("good image")



def main():
    root.geometry("550x300+30+30")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()