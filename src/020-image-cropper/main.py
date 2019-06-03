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
conf = Configuration(inifile=os.path.join(dir_path, "..", "config.ini"))


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
#        bindings.SetFunction("py_search_stop_callback", self.search_stop_callback)
        self.browser.SetJavascriptBindings(bindings)

        if MAC:
            from Cocoa import NSRunningApplication, NSApplicationActivateIgnoringOtherApps
            app = NSRunningApplication.runningApplicationWithProcessIdentifier_(os.getpid())
            app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)

    # Called if the user pressed the "search" button. Now the current active search term is posted
    # to the "queue_search_query" queue. The "search" thread picks up the new search term and starts crawling
    # images related to the new search term
    def search_start_callback(self, search_term):
        pass

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
