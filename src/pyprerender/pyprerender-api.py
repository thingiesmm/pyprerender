#!/usr/bin/env python

import os

import uvicorn
from starlette.applications import Starlette
from starlette.middleware.gzip import GZipMiddleware
from starlette.responses import Response
from pyprerender import ParseHTMLEventHandler, Chrome


CHROME_OPTIONS = {
    'browser_debugging_port': '9222',
    'chrome_location': os.environ.get(
        'CHROME_LOCATION', '/usr/bin/google-chrome-stable'
    ),
    'chrome_params': ['-window-size=1920,1080'],
}

chrome = Chrome(options=CHROME_OPTIONS)

app = Starlette(debug=False)
app.add_middleware(GZipMiddleware, minimum_size=1000)

handler_kwargs = {'enable_stopping': True}


@app.route('/render', methods=['POST', 'GET'])
async def render(request):
    if request.method == 'GET':
        params = request.query_params
    else:
        params = await request.json()

    print('___REQUEST__')
    print(params)
    url = params.get('url')
    tab = chrome.new_tab()

    chrome.navigate(
        tab,
        url,
        event_handler=ParseHTMLEventHandler,
        event_handler_kwargs=handler_kwargs,
        tab_wait=5,
    )
    tab.wait(3)
    prerender_content = tab.prerender_content
    chrome.close_tab(tab)
    return Response(prerender_content)


if __name__ == '__main__':
    uvicorn.run(
        'pyprerender-api:app', host='0.0.0.0', port=int(os.environ.get('PORT', 8080))
    )
