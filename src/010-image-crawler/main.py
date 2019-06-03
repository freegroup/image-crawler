#from sys import platform as sys_pf
#if sys_pf == 'darwin':
#    import matplotlib
#    matplotlib.use("TkAgg")
import queue
import os
import platform
import sys
import base64

from cefpython3 import cefpython as cef
from PIL import ImageTk, Image, ImageOps
from pydoc import locate
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
accepted_worker = ImageAppraiser(queue_img_fetched, queue_img_appraised, queue_img_skipped)
accepted_worker.start()

AcceptedImageWorker = locate(conf.impl_accepted())
accepted_worker = AcceptedImageWorker(queue_img_accepted)
accepted_worker.start()

SkippedImageWorker = locate(conf.impl_skipped())
skipped_worker = SkippedImageWorker(queue_img_skipped)
skipped_worker.start()


# Very basic UI for the image search and selection.
#
class App():

    def __init__(self):

        self.image_current = None
        self.check_versions()

        window_info = cef.WindowInfo()
        rect = [150, 250, 950, 700]
        window_info.SetAsChild(0, rect)

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.browser = cef.CreateBrowserSync(
            window_info,
            url='file://' + os.path.join(cur_dir, "ui", "index.html")
        )

        self.browser.SetClientHandler(self.load_handler())
        bindings = cef.JavascriptBindings()
        bindings.SetFunction("py_search_stop_callback", self.search_stop_callback)
        bindings.SetFunction("py_search_start_callback", self.search_start_callback)
        bindings.SetFunction("py_skip_image_callback", self.skip_image_callback)
        bindings.SetFunction("py_keep_image_callback", self.keep_image_callback)
        bindings.SetFunction("py_check_image_callback", self.check_for_image_callback)
        self.browser.SetJavascriptBindings(bindings)

        if MAC:
            from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
            app = NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)

    # Called if the user pressed the "search" button. Now the current active search term is posted
    # to the "queue_search_query" queue. The "search" thread picks up the new search term and starts crawling
    # images related to the new search term
    def search_start_callback(self, search_term):
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

    def search_stop_callback(self):
        conf.search_term = None
        self.image_current = None
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
        try:
            while True:
                queue_img_appraised.get_nowait()
        except queue.Empty:
            pass

    # Called of the user press the button or the configured key for "skipping" an image.
    # The method moves the current display image into the "skipped" queue.
    # The worker thread picks up this image and moves them into the related folder
    #
    def skip_image_callback(self):
        if self.image_current is not None:
            if 'md5' in self.image_current.keys():
                queue_img_skipped.put(self.image_current)
            self.display_next_image()

    # Called of the user press the button or the configured key for "keep" an image.
    # The method moves the current display image into the "keep" queue.
    # The worker thread picks up this image and moves them into the related folder
    #
    def keep_image_callback(self):
        if self.image_current is not None:
            if 'md5' in self.image_current.keys():
                queue_img_accepted.put(self.image_current)
            self.display_next_image()

    def check_for_image_callback(self):
        if queue_img_appraised.qsize() > 0 and self.image_current == None:
            self.display_next_image()
        if(queue_img_urls.qsize() < queue_img_urls.maxsize):
            self.browser.ExecuteFunction("js_set_counter", "counter_candidates", queue_img_urls.qsize())
        else:
            self.browser.ExecuteFunction("js_set_counter", "counter_candidates", ">"+str(queue_img_urls.maxsize))

        if(queue_img_appraised.qsize() < queue_img_appraised.maxsize):
            self.browser.ExecuteFunction("js_set_counter", "counter_review", queue_img_appraised.qsize())
        else:
            self.browser.ExecuteFunction("js_set_counter", "counter_review", ">"+str(queue_img_appraised.maxsize))

        self.browser.ExecuteFunction("js_set_counter", "counter_pool", inventory.count_already_accepted())

    # Load the next image from the queue and display them in the UI
    #
    def display_next_image(self):
        if queue_img_appraised.qsize()>0  :
            self.image_current = queue_img_appraised.get()
            #self.skip_button.state(["!disabled"])   # Disable the button.
            #self.keep_button.state(["!disabled"])  # Enable the button.
        else:
            self.image_current = None
            #self.skip_button.state(["disabled"])   # Disable the button.
            #self.keep_button.state(["disabled"])  # Enable the button.

        img =  self.image_current["image"]
        ext =img.format
        buffered = BytesIO()
        img.save(buffered, ext)
        img_str = base64.b64encode(buffered.getvalue())
        image_src = "data:{0};base64,{1}".format(conf.image_descriptor_by_type(ext), img_str.decode("utf-8"))
        self.browser.ExecuteFunction("js_set_image", image_src)

    class load_handler(object):
        def OnLoadEnd(self, browser, **_):
            pass
            #browser.ExecuteFunction("js_init_image_check_timer")

        def DoClose(self, browser):
            cef.QuitMessageLoop()


    def check_versions(self):
        ver = cef.GetVersion()
        print("CEF Python {ver}".format(ver=ver["version"]))
        print("Chromium {ver}".format(ver=ver["chrome_version"]))
        print("CEF {ver}".format(ver=ver["cef_version"]))
        print("Python {ver} {arch}".format(
            ver=platform.python_version(),
            arch=platform.architecture()[0]))
        assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this"


if __name__ == '__main__':
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    app = App()
    cef.MessageLoop()
