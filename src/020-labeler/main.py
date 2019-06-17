import queue
import os
import platform
import sys
import base64
import json

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

# Images which have not yet been labeled
# (filled by the "reader" )
queue_candidates = []

# The "Reader" and "Writer" are implemented as plugin. It is possible
# to read/write from an S3 storage without changing the UI - just by writing new plugins
#
ImageWriterWorker = locate(conf.impl_exporter())
writer_worker = ImageWriterWorker()

ImageReaderWorker = locate(conf.impl_reader())
reader_worker = ImageReaderWorker(queue_candidates)


class App():
    def __init__(self):
        self.check_versions()
        self.current_image_index = 0
        self.current_image_meta = None

        window_info = cef.WindowInfo()
        rect = [150, 250, 1150, 700]
        window_info.SetAsChild(0, rect)

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        self.browser = cef.CreateBrowserSync(
            window_info,
            url='file://' + os.path.join(cur_dir, "ui", "index.html")
        )

        self.browser.SetClientHandler(self.load_handler())
        bindings = cef.JavascriptBindings()
        bindings.SetFunction("py_next_click_callback", self.py_next_click_callback)
        bindings.SetFunction("py_back_click_callback", self.py_back_click_callback)
        bindings.SetFunction("py_set_labels", self.py_set_labels)
        self.browser.SetJavascriptBindings(bindings)

        # bring the window on top. For some reasons the cefwindow start in the background...
        #
        if MAC:
            from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
            app = NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)

    # Called if the user pressed the "search" button. Now the current active search term is posted
    # to the "queue_search_query" queue. The "search" thread picks up the new search term and starts crawling
    # images related to the new search term
    #
    def py_back_click_callback(self, labels):
        self.current_image_meta["labels"] = labels
        writer_worker.write(self.current_image_meta)
        self.current_image_index = self.current_image_index-1
        self.display_image()

    # Called if the user pressed the "search" button. Now the current active search term is posted
    # to the "queue_search_query" queue. The "search" thread picks up the new search term and starts crawling
    # images related to the new search term
    def py_next_click_callback(self, labels):
        self.current_image_meta["labels"] = labels
        writer_worker.write(self.current_image_meta)
        self.current_image_index = self.current_image_index+1
        self.display_image()

    # Called if the user changes the labels in the input fields.
    # New values are stored in the property file
    #
    def py_set_labels(self, labels):
        conf.ui("labels", ",".join(labels))

    # Send the image with the "current_image_index" as base64 to the HTML UI
    #
    def display_image(self):
        self.current_image_meta = reader_worker.read(self.current_image_index)
        width = self.current_image_meta["width"]
        height = self.current_image_meta["height"]
        labels = self.current_image_meta["labels"]
        format = self.current_image_meta["format"]
        # convert the image into a js image source URL.
        buffered = BytesIO()
        self.current_image_meta["image"].save(buffered, format)
        img_str = base64.b64encode(buffered.getvalue())
        image_src = "data:{0};base64,{1}".format(conf.image_descriptor_by_type(format), img_str.decode("utf-8"))
        # show the new loaded image in the UI
        self.browser.ExecuteFunction("js_set_image", image_src, width, height, labels)

    # read the configuration for the shortcuts and the labels from the configuration file and
    # send them to the js UI
    #
    def init_ui(self):
        self.display_image()
        self.browser.ExecuteFunction("js_set_labels", conf.ui("labels").split(","))
        self.browser.ExecuteFunction("js_set_navigation_shortcuts",
                                     conf.ui("shortcut-next"),
                                     conf.ui("shortcut-back"),
                                     conf.ui("shortcut-label-1"),
                                     conf.ui("shortcut-label-2"),
                                     conf.ui("shortcut-label-3")
                                     )

    class load_handler(object):
        def OnLoadEnd(self, browser, **_):
            global app
            app.init_ui()
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
