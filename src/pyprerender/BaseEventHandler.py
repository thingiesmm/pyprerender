import threading


class BaseEventHandler(object):
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
