from src.pyprerender.Chrome import Chrome
from src.pyprerender.ScreenshotHandler import ScreenshotEventHandler
import time

if __name__ == '__main__':
    options = {
        'browser_debugging_port': '9222'
    }
    chrome = Chrome(options=options)
    time.sleep(2)
    chrome.connect()
    tab = chrome.new_tab()
    chrome.navigate(tab, 'https://google.com', event_handler=ScreenshotEventHandler)
