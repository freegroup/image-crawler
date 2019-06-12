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

# Some worker queue to handle the different threads for searching, loading, grouping,...
#
queue_candidates = []

# reads the images from the "queue_output" and exports them into the named directory
#ImageWriterWorker = locate(conf.impl_exporter())
#writer_worker = ImageWriterWorker(queue_output)
#writer_worker.start()


# stores the readed images into the "queue_input" for further processing
ImageReaderWorker = locate(conf.impl_reader())
reader_worker = ImageReaderWorker(queue_candidates)
reader_worker.start()


# Very basic UI for the image search and selection.
#
class App():
    def __init__(self):
        self.check_versions()
        self.current_index = 0

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
        bindings.SetFunction("py_on_next_click_callback", self.on_next_click_callback)
        bindings.SetFunction("py_on_last_click_callback", self.on_last_click_callback)
        self.browser.SetJavascriptBindings(bindings)

        if MAC:
            from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
            app = NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)

    # Called if the user pressed the "search" button. Now the current active search term is posted
    # to the "queue_search_query" queue. The "search" thread picks up the new search term and starts crawling
    # images related to the new search term
    def on_last_click_callback(self, labels):

        print(labels)
        self.current_index = self.current_index-1
        self.display_image()

    # Called if the user pressed the "search" button. Now the current active search term is posted
    # to the "queue_search_query" queue. The "search" thread picks up the new search term and starts crawling
    # images related to the new search term
    def on_next_click_callback(self, labels):
        print(labels)
        current_json = queue_candidates[self.current_index]
        with open(current_json) as json_file:
            image_meta = json.load(json_file)
            image_meta["labels"] = labels
        with open(current_json, 'w') as outfile:
            json.dump(image_meta, outfile, indent=4)

        self.current_index = self.current_index+1
        self.display_image()

    # Called if the user pressed the "search" button. Now the current active search term is posted
    # to the "queue_search_query" queue. The "search" thread picks up the new search term and starts crawling
    # images related to the new search term
    def display_image(self):
        next_json = queue_candidates[self.current_index]

        with open(next_json) as json_file:
            image_meta = json.load(json_file)
            md5 = image_meta["md5"]
            if 'labels' in image_meta.keys():
                labels = image_meta["labels"]
            else:
                labels = "[]"
            ext = image_meta["format"].lower()
            path = next_json.replace("json", ext)
            img = Image.open(path)
            width, height = img.size
            buffered = BytesIO()
            img.save(buffered, ext)
            img_str = base64.b64encode(buffered.getvalue())
            image_src = "data:{0};base64,{1}".format(conf.image_descriptor_by_type(ext), img_str.decode("utf-8"))
            self.browser.ExecuteFunction("js_set_image", image_src, width, height, labels)

    class load_handler(object):
        def OnLoadEnd(self, browser, **_):
            global app
            app.display_image()
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
