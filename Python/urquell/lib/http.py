# -*- coding: utf-8 -*-
from urquell.http import Module
from urquell.lib import lib
from urquell.invocation import path_args
from google.appengine.api.urlfetch import fetch


http = Module(lib, 'http', """HTTP functions.""")


def get(url):
    """
        <p>Does a HTTP get on the specified URL and returns the response. This will only return the body text if the resource is text.</p>
        <p>If the encoding isn't properly specified in the target page's Content-Type then it's quite likely to error.</p>
    """
    if url:
        response = fetch(url, deadline=10)
        headers = dict([(k, v) for k, v in response.headers.items()]);
        mime, encoding = headers.get('content-type', '').split(';')
        if len(encoding):
            charset = encoding.split('=')[1]
        if mime.startswith('text/'):
            return dict(
                body = response.content.decode(charset),
                headers = headers,
            )
        else:
            return dict(
                body = None,
                headers = headers,
            )
    else:
        return None
http.pure(get, [
])
