from src.pyprerender import BaseEventHandler
import json


class ParseHTMLEventHandler(BaseEventHandler):
    def __init__(self, browser, tab, enable_scrolling=False, enable_stopping=True):
        super().__init__(browser, tab)
        self.first_time = True
        self.enable_scrolling = enable_scrolling
        self.enable_stopping = enable_stopping

    def frame_started_loading(self, frameId):
        super().frame_started_loading(frameId)

    def frame_stopped_loading(self, frameId):
        super().frame_stopped_loading(frameId)
        if self.first_time and self.enable_scrolling:
            layout_metrcs = self.tab.Page.getLayoutMetrics()
            content_size = layout_metrcs['contentSize']
            page_size = layout_metrcs['visualViewport']
            for i in range(page_size['clientHeight'], content_size['height'], page_size['clientHeight']):
                self.tab.Runtime.evaluate(expression=f'window.scrollTo(0, {i})')
                print('scrolling', i)
                self.tab.wait(1)
            self.tab.wait(2)
            self.first_time = False
        else:
            self.parse_html(self.tab)
            if self.start_frame == frameId:
                self.tab.Page.stopLoading()
            if self.enable_stopping:
                self.tab.stop()

    @staticmethod
    def parse_html(tab):
        response = tab.Runtime.evaluate(expression="document.firstElementChild.outerHTML")
        tab.prerender_content = response['result']['value']
        response = tab.Runtime.evaluate(
            expression='document.doctype && JSON.stringify({name: document.doctype.name, systemId: document.doctype.systemId, publicId: document.doctype.publicId})'
        )
        doctype = ''
        if response and response['result'] and response['result']['value']:
            obj = {'name': 'html'}
            try:
                obj = json.loads(response['result']['value'])
            except:
                pass
            finally:
                doctype = "<!DOCTYPE " + obj['name'] \
                          + obj['publicId'] + '"' if 'publicId' in obj else '' \
                                                                            + ' SYSTEM' if (
                        'publicId' not in obj and 'systemId' in obj) else '' \
                                                                          + ' "' + obj[
                                                                              'systemId'] + '"' if 'systemId' in obj else '' \
                                                                                                                          + '">'

        tab.prerender_content = doctype + tab.prerender_content

