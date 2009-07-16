# -*- coding: utf-8 -*-
import urllib
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api.urlfetch import fetch

from jsonrpc.json import dumps, loads

"""
Example record

{
ihash: '3jdHes',
url: 'http://urquell-fn.appspot.com/lib/sub/3/4.json
}
"""

class Invocation(db.Model):
  ihash = db.StringProperty(required=True)
  url = db.StringProperty(required=True)

def invoke(path, request, module, fn):
    ihash = store_invocation(request.url)
    parts = path[len(module.path()) + len(fn.func_name) + 2:].split('/')
    call_trace = [resolver_path(str(i)) for i in parts]
    args = [x for u, x in call_trace]
    kwargs = dict(
        [(str(k), resolver_query(request.GET[k])) for k in request.GET]
    )
    object = {
        'hash': u'*%s' % unicode(ihash),
        'name': '%s/%s' % (module.path(), fn.func_name),
        'args': [u for u, x in call_trace],
        'path': path,
        'value': fn(*args, **kwargs),
        'headers': dict([(k, unicode(v)) for k, v in request.headers.items()]),
    }
    json = dumps(object)
    memcache.add(ihash, json, 300)
    return json, object

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

import re, urllib, os

REAL = re.compile('^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')
FUNCTION = re.compile('^=')
def resolver_path(value):
    value = urllib.unquote(value)
    if value.startswith('**'):
        value = value[1:]
    elif value.startswith('*'):
        return resolve_function(value[1:])

    if value.isdigit():
        return (value, int(value))
    elif REAL.match(value):
        return (value, float(value))
    return (value, value)

def resolver_query(value):
    return value

def resolve_function(value):
    dest = Invocation.gql("WHERE ihash = :1", value).fetch(1)
    if not len(dest):
        raise Exception("Unable to resolve function invocation. Invocation hash: %s" % value)
    url = dest[0].url
    json = memcache.get(value)
    if not json:
        return (url, execute(url)['value'])
    else:
        return (url, loads(json)['value'])

def path_args(path):
    return '/'.join([urllib.quote(unicode(p), '') for p in path])
