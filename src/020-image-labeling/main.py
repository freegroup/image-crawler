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

# Platforms
WINDOWS = (platform.system() == "Windows")
LINUX = (platform.system() == "Linux")
MAC = (platform.system() == "Darwin")


dir_path = os.path.dirname(os.path.realpath(__file__))

# Load the app configuration
#
conf = Configuration(inifile=os.path.join(dir_path, "config.ini"))

# Some worker queuea to handle the different threads for searching, loading, grouping,...
#
queue_candidates = queue.Queue()
queue_loaded = queue.Queue(maxsize=10)
queue_output = queue.Queue(maxsize=10)


# reads the images from the "queue_output" and exports them into the named directory
#ImageWriterWorker = locate(conf.impl_exporter())
#writer_worker = ImageWriterWorker(queue_output)
#writer_worker.start()


# stores the readed images into the "queue_input" for further processing
ImageReaderWorker = locate(conf.impl_reader())
reader_worker = ImageReaderWorker(queue_candidates, queue_loaded)
reader_worker.start()


# Very basic UI for the image search and selection.
#
class App():
    def __init__(self):
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
        bindings.SetFunction("py_search_start_callback", self.search_start_callback)
        self.browser.SetJavascriptBindings(bindings)

        if MAC:
            from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
            app = NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)

    # Called if the user pressed the "search" button. Now the current active search term is posted
    # to the "queue_search_query" queue. The "search" thread picks up the new search term and starts crawling
    # images related to the new search term
    def search_start_callback(self, search_term):
        self.image_current = queue_loaded.get()
        img = self.image_current["image"]
        ext = img.format
        width, height = img.size
        buffered = BytesIO()
        img.save(buffered, ext)
        img_str = base64.b64encode(buffered.getvalue())
        image_src = "data:{0};base64,{1}".format(conf.image_descriptor_by_type(ext), img_str.decode("utf-8"))
        self.browser.ExecuteFunction("js_set_image", image_src, width, height)

    # Load the next image from the queue and display them in the UI
    #
    def display_next_image(self):


        img = self.image_current["image"]
        ext = img.format
        buffered = BytesIO()
        img.save(buffered, ext)
        img_str = base64.b64encode(buffered.getvalue())
        image_src = "data:{0};base64,{1}".format(conf.image_descriptor_by_type(ext), img_str.decode("utf-8"))
        self.browser.ExecuteFunction("js_set_image", image_src)

    class load_handler(object):
        def OnLoadEnd(self, browser, **_):
            pass

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
