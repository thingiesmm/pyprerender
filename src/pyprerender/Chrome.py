import pychrome
import subprocess
import time


class Chrome:
    def __init__(self, options):
        """
        :param options:
            options['chrome_params']  - list, additional chrome params
            options['override_chrome_params'] - bool, whether 'chrome_params' replaces or extends default chrome params
            options['browser_debugging_port'] - browser debugging port

        """
        self.options = options
        self.chrome_location = options['chrome_location']
        base_params = [
            self.chrome_location,
            '--remote-debugging-port=' + self.options['browser_debugging_port'],
        ]
        default_params = [
            '--headless',
            '--disable-gpu',
            '--hide-scrollbars',
        ]
        override_chrome_params = False
        if 'override_chrome_params' in options:
            override_chrome_params = options['override_chrome_params']

        if override_chrome_params:
            params = base_params
        else:
            params = base_params + default_params
        if 'chrome_params' in options:
            params += options['chrome_params']
        self.chrome_process = subprocess.Popen(params)
        self.browser = None
        time.sleep(1)
        self.connect()

    def connect(self):
        self.browser = pychrome.Browser(
            url='http://127.0.0.1:' + self.options['browser_debugging_port']
        )

    def new_tab(self):
        tab = self.browser.new_tab()
        return tab

    def close_tab(self, tab):
        try:
            self.browser.close_tab(tab)
        except:  # noqa
            pass

    def navigate(
        self, tab, url, event_handler=None, event_handler_kwargs=None, tab_wait=10
    ):
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
