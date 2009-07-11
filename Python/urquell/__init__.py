# -*- coding: utf-8 -*-
from jsonrpc.json import dumps, loads
from google.appengine.api.urlfetch import fetch


class Responder(object):
    urls = []


def execute(url):
    return loads(fetch(url).content)
