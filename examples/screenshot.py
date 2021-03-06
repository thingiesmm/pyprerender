from pyprerender import Chrome
import time
import threading
import base64
import os


class ScreenshotEventHandler(object):
    screen_lock = threading.Lock()

    def __init__(self, browser, tab, directory='./'):
        self.browser = browser
        self.tab = tab
        self.start_frame = None
        self.directory = directory

    def frame_started_loading(self, frameId):
        if not self.start_frame:
            self.start_frame = frameId

    def frame_stopped_loading(self, frameId):
        if self.start_frame == frameId:
            self.tab.Page.stopLoading()

            with self.screen_lock:
                # must activate current tab
                print(self.browser.activate_tab(self.tab.id))

                try:
                    data = self.tab.Page.captureScreenshot()
                    with open(os.path.join(self.directory, "%s.png") % time.time(), "wb") as fd:
                        fd.write(base64.b64decode(data['data']))
                finally:
                    self.tab.stop()


if __name__ == '__main__':
    options = {
        'browser_debugging_port': '9222',
        'chrome_location': '/usr/bin/google-chrome-stable'
    }
    chrome = Chrome(options=options)
    tab = chrome.new_tab()
    chrome.navigate(tab, 'https://google.com', event_handler=ScreenshotEventHandler)
