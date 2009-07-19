# -*- coding: utf-8 -*-
import os, urllib
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api.urlfetch import fetch

from jsonrpc.json import dumps, loads


class ErrorTrace(Exception):
    def __init__(self, message, trace = {}):
        self.message = message
        self.trace = trace


class Invocation(db.Model):
  ihash = db.StringProperty(required=True)
  url = db.StringProperty(required=True)

def invoke(responder, module, fn, *path, **kwargs):
    from urquell.value import resolve_part
    ihash = store_invocation(responder.request.url)
    responder.object['hash'] = u'*%s' % unicode(ihash)
    responder.object['name'] = '%s/%s' % (module.path(), fn.func_name)
    call_trace = [resolve_part(str(i)) for i in path]
    kwargs = dict(
        [(str(k), resolve_part(responder.request.GET[k])) for k in responder.request.GET]
    )
    args = [x for u, x in call_trace]
    responder.object['args'] = [u for u, x in call_trace]
    responder.object['value'] = fn(*args, **kwargs)
    json = dumps(responder.object)
    if responder.object.has_key('value'):
        memcache.add(ihash, json, 300)
    return json, responder.object

def execute(url):
    if url:
        json = fetch(url, headers={
            'X-Requested-With': 'XMLHttpRequest',
        }).content
        try:
            return loads(json)
        except Exception, e:
            raise Exception(json)
    else:
        return None

def store_invocation(a_url):
    invocation = Invocation.gql("WHERE url = :1", a_url).fetch(1)
    if not len(invocation):
        def gen_ihash():
            ihash = os.urandom(6).encode("base64")[:8].replace('+', '-').replace('/', '_')
            invocation = Invocation.gql("WHERE ihash = :1", ihash).fetch(1)
            if len(invocation):
                return gen_ihash()
            return ihash
        ihash = gen_ihash()
        invocation = Invocation(ihash=ihash,url=a_url)
        db.put(invocation)
        return ihash
    else:
        return invocation[0].ihash
