import pychrome
import subprocess
import time


class Chrome:
    def __init__(self, options):
        self.options = options
        self.chrome_location = options['chrome_location']
        params = [self.chrome_location,
                  '--headless',
                  '--disable-gpu',
                  '--remote-debugging-port=' + self.options['browser_debugging_port'],
                  '--hide-scrollbars',
                  ]
        if 'chrome_params' in options:
            params.extend(options['chrome_params'])
        self.chrome_process = subprocess.Popen(params)
        self.browser = None
        time.sleep(1)
        self.connect()

    def connect(self):
        self.browser = pychrome.Browser(url='http://127.0.0.1:' + self.options['browser_debugging_port'])

    def new_tab(self):
        tab = self.browser.new_tab()
        return tab

    def close_tab(self, tab):
        try:
            self.browser.close_tab(tab)
        except:
            pass

    def navigate(self, tab, url, event_handler=None, event_handler_kwargs=None, tab_wait=10):
        # start the tab
        if event_handler:
            if event_handler_kwargs:
                eh = event_handler(self.browser, tab, **event_handler_kwargs)
            else:
                eh = event_handler(self.browser, tab)
            tab.Page.frameStartedLoading = eh.frame_started_loading
            tab.Page.frameStoppedLoading = eh.frame_stopped_loading

        tab.start()

        # tab.Page.stopLoading()
        # call method
        tab.Page.enable()
        tab.Network.enable()
        # call method with timeout
        tab.Page.navigate(url=url)
        # wait for loading
        tab.wait(tab_wait)

        # stop the tab (stop handle events and stop recv message from chrome)
        # tab.stop()

        # close tab
        # self.browser.close_tab(tab)

    def __del__(self):
        self.chrome_process.kill()
