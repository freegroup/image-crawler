import tkinter as tk    # either in python 2 or in python 3
from PIL import Image, ImageTk


def download_images():
    # In order to fetch the image online
    try:
        import urllib.request as url
    except ImportError:
        import urllib as url
    url.urlretrieve("https://i.stack.imgur.com/IgD2r.png", "lenna.png")
    url.urlretrieve("https://i.stack.imgur.com/sML82.gif", "lenna.gif")


if __name__ == '__main__':
    download_images()
    root = tk.Tk()
    widget = tk.Label(root, compound='top')
    widget.lenna_image_png = ImageTk.PhotoImage(Image.open("lenna.png"))
    widget.lenna_image_gif = ImageTk.PhotoImage(Image.open("lenna.gif"))
    try:
        widget['text'] = "Lenna.png"
        widget['image'] = widget.lenna_image_png
    except:
        widget['text'] = "Lenna.gif"
        widget['image'] = widget.lenna_image_gif
    widget.pack()
    root.mainloop()