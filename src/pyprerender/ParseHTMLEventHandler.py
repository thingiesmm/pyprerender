from src.pyprerender import BaseEventHandler
import json


class ParseHTMLEventHandler(BaseEventHandler):
    def __init__(self, browser, tab):
        super().__init__(browser, tab)

    def frame_stopped_loading(self, frameId):
        super().frame_stopped_loading(frameId)
        self.parse_html(self.tab)
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

