import pychrome
import subprocess
import time


class Chrome:
    def __init__(self, options):
        self.options = options
        self.chrome_location = '/usr/bin/google-chrome-stable'
        self.chrome_process = subprocess.Popen([self.chrome_location,
                                                '--headless',
                                                '--disable-gpu',
                                                '--remote-debugging-port=' + self.options['browser_debugging_port'],
                                                '--hide-scrollbars',
                                                ])
        self.browser = None
        time.sleep(2)
        self.connect()

    def connect(self):
        self.browser = pychrome.Browser(url='http://127.0.0.1:' + self.options['browser_debugging_port'])

    def new_tab(self):
        return self.browser.new_tab()

    def navigate(self, tab, url, event_handler=None):
        # start the tab
        if event_handler:
            eh = event_handler(self.browser, tab)
            tab.Page.frameStartedLoading = eh.frame_started_loading
            tab.Page.frameStoppedLoading = eh.frame_stopped_loading

        tab.start()

        tab.Page.stopLoading()
        # call method
        tab.Page.enable()
        # call method with timeout
        tab.Page.navigate(url=url)

        # wait for loading
        tab.wait(10)

        # stop the tab (stop handle events and stop recv message from chrome)
        tab.stop()

        # close tab
        self.browser.close_tab(tab)
