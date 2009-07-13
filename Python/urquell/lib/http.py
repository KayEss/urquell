# -*- coding: utf-8 -*-
from urquell.http import Module
from urquell.lib import lib
from urquell.invocation import path_args
from google.appengine.api.urlfetch import fetch


http = Module(lib, 'http', """HTTP functions.""")


def get(url, *path, **kwargs):
    """Does a HTTP get on the specified URL and returns the response."""
    if url:
        response = fetch(url)
        return dict(
            body = response.content,
            headers = response.headers,
        )
    else:
        return None
http.pure(get, [
])
