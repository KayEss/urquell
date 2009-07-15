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
        headers = dict([(k, v) for k, v in response.headers.items()])
        mime, encoding = headers.get('Content-Type', ';').split(';')
        if len(encoding):
            charset = encoding.split('=')[1]
        if mime.startswith('text/'):
            return dict(
                status = response.status_code,
                body = response.content.decode(charset),
                headers = headers,
            )
        else:
            return dict(
                status = response.status_code,
                body = None,
                headers = headers,
            )
    else:
        return None
http.pure(get, [
    '*zmHOYaYg'
])

def headers(url):
    """
        <p>Returns only the HTTP headers for a request performed through HEAD request.</p>
    """
    if url:
        response = fetch(url, method="HEAD", deadline=10)
        return dict([(k, v) for k, v in response.headers.items()])
http.pure(headers, [
    '*zmHOYaYg'
])

def status(url):
    """
        <p>Returns only the status code for a request performed through HEAD request.</p>
    """
    if url:
        response = fetch(url, method="HEAD", deadline=10)
        return response.status_code
http.pure(status, [
    '*zmHOYaYg'
])
