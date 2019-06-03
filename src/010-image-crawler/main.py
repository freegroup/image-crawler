#from sys import platform as sys_pf
#if sys_pf == 'darwin':
#    import matplotlib
#    matplotlib.use("TkAgg")
from cefpython3 import cefpython as cef
import ctypes
import queue
import tkinter as tk
from pydoc import locate
from PIL import ImageTk, Image, ImageOps
import os
import platform
import sys
import base64
from io import BytesIO

from configuration import Configuration
from persistence.hashes import MD5Inventory

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")


dir_path = os.path.dirname(os.path.realpath(__file__))

# Load the app configuration
#
conf = Configuration(inifile=os.path.join(dir_path, "..", "config.ini"))
inventory = MD5Inventory()

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
class App(tk.Frame):

    def __init__(self, master):
        # Root
        master.geometry("900x640")
        tk.Grid.rowconfigure(master, 0, weight=1)
        tk.Grid.columnconfigure(master, 0, weight=1)

        tk.Frame.__init__(self, master)

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_root_configure)

        self.check_versions()

        self.image_loading = { "image": Image.open(os.path.join(dir_path, "loading.png"))}


        # BrowserFrame
        self.browser_frame = BrowserFrame(self)
        self.browser_frame.grid(row=0, column=0, sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

        #rect = [0, 0, self.winfo_width(), self.winfo_height()]
        #window_info = cef.WindowInfo()
        #window_info.SetAsChild(self.get_window_handle(), rect)

        #cur_dir = os.path.dirname(os.path.abspath(__file__))
        #self.browser = cef.CreateBrowserSync(
        #    window_info,
        #    url='file://' + os.path.join(cur_dir, "ui", "index.html")
        #)

        #self.browser.SetClientHandler(self.load_handler())
        #bindings = cef.JavascriptBindings()
        #bindings.SetFunction("py_search_image_callback", self.search_image_callback)
        #bindings.SetFunction("py_skip_image_callback", self.skip_image_callback)
        #bindings.SetFunction("py_keep_image_callback", self.keep_image_callback)
        #bindings.SetFunction("py_check_image_callback", self.check_for_image_callback)
        #self.browser.SetJavascriptBindings(bindings)


    # Called if the user pressed the "search" button. Now the current active search term is posted
    # to the "queue_search_query" queue. The "search" thread picks up the new search term and starts crawling
    # images related to the new search term
    #
    def search_image_callback(self, search_term):
        conf.search_term = search_term
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

    def check_for_image_callback(self):
        if queue_img_appraised.qsize()>0 and self.image_current == self.image_loading :
            self.display_next_image()
        self.browser.ExecuteFunction("js_set_counter", "counter_candidates", queue_img_urls.qsize())
        self.browser.ExecuteFunction("js_set_counter", "counter_review", queue_img_appraised.qsize())
        self.browser.ExecuteFunction("js_set_counter", "counter_pool", inventory.count_already_accepted())

    # Load the next image from the queue and display them in the UI
    #
    def display_next_image(self):
        if queue_img_appraised.qsize()>0  :
            self.image_current = queue_img_appraised.get()
            #self.skip_button.state(["!disabled"])   # Disable the button.
            #self.keep_button.state(["!disabled"])  # Enable the button.
        else:
            self.image_current = self.image_loading
            #self.skip_button.state(["disabled"])   # Disable the button.
            #self.keep_button.state(["disabled"])  # Enable the button.


        img =  self.image_current["image"]
        ext =img.format
        buffered = BytesIO()
        img.save(buffered, ext)
        img_str = base64.b64encode(buffered.getvalue())
        image_src = "data:{0};base64,{1}".format(self.get_descriptor_by_type(ext), img_str.decode("utf-8"))
        self.browser.ExecuteFunction("js_set_image", image_src)


    class load_handler(object):
        def OnLoadEnd(self, browser, **_):
            browser.ExecuteFunction("js_init_image_check_timer")

    def on_closing(self):
        self.__root.destroy()

    def get_descriptor_by_type(self, ext):
        options = {
            "JPEG": "image/jpeg",
            "PNG": "image/png",
            "GIF": "image/gif"
        }
        k = options.get(ext)
        if k is None:
            raise Exception("No support for ["+ext+"] Only Jpeg, Png and Gif images are supported.")
        return k

    def check_versions(self):
        ver = cef.GetVersion()
        print("CEF Python {ver}".format(ver=ver["version"]))
        print("Chromium {ver}".format(ver=ver["chrome_version"]))
        print("CEF {ver}".format(ver=ver["cef_version"]))
        print("Python {ver} {arch}".format(
            ver=platform.python_version(),
            arch=platform.architecture()[0]))
        assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"

    def on_root_configure(self, _):
        if self.browser_frame:
            self.browser_frame.on_root_configure()

    def on_configure(self, event):
         if self.browser_frame:
            width = event.width
            height = event.height
            self.browser_frame.on_mainframe_configure(width, height)

    def on_focus_in(self, _):
        pass

    def on_focus_out(self, _):
        pass

    def on_close(self):
        if self.browser_frame:
            self.browser_frame.on_root_close()
        self.master.destroy()

    def get_browser(self):
        if self.browser_frame:
            return self.browser_frame.browser
        return None

    def get_browser_frame(self):
        if self.browser_frame:
            return self.browser_frame
        return None

    def setup_icon(self):
        pass



class BrowserFrame(tk.Frame):

    def __init__(self, master):
        self.closing = False
        self.browser = None
        tk.Frame.__init__(self, master)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)
        self.focus_set()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="https://www.google.com/")
        assert self.browser
 #       self.browser.SetClientHandler(LoadHandler(self))
 #       self.browser.SetClientHandler(FocusHandler(self))
        self.message_loop_work()

    def get_window_handle(self):
        if self.winfo_id() > 0:
            return self.winfo_id()
        elif MAC:
            # On Mac window id is an invalid negative value (Issue #308).
            # This is kind of a dirty hack to get window handle using
            # PyObjC package. If you change structure of windows then you
            # need to do modifications here as well.
            # noinspection PyUnresolvedReferences
            from AppKit import NSApp
            # noinspection PyUnresolvedReferences
            import objc
            # Sometimes there is more than one window, when application
            # didn't close cleanly last time Python displays an NSAlert
            # window asking whether to Reopen that window.
            # noinspection PyUnresolvedReferences
            return objc.pyobjc_id(NSApp.windows()[-1].contentView())
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def on_root_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()

    def on_mainframe_configure(self, width, height):
        if self.browser:
            if WINDOWS:
                ctypes.windll.user32.SetWindowPos(
                    self.browser.GetWindowHandle(), 0,
                    0, 0, width, height, 0x0002)
            elif LINUX:
                self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        if self.browser:
            self.browser.SetFocus(True)

    def on_focus_out(self, _):
        if self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        if self.browser:
            self.browser.CloseBrowser(True)
            self.browser = None
        self.destroy()


if __name__ == '__main__':
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    root = tk.Tk()
    app = App(root)
    # Tk must be initialized before CEF otherwise fatal error (Issue #306)
    cef.Initialize()
    app.mainloop()
    cef.Shutdown()

