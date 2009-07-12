# -*- coding: utf-8 -*-
from google.appengine.ext import db
from google.appengine.api import memcache

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

def store_invocation(a_url):
    def gen_ihash():
        ihash = os.urandom(16).encode("base64")[:6]
        invocation = Invocation.gql("WHERE ihash = '%s'" % ihash).fetch(1)
        if len(invocation):
            return gen_ihash()
        return ihash
    invocation = Invocation.gql("WHERE url = '%s'" % a_url).fetch(1)
    if not len(invocation):
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
    if FUNCTION.match(value):
        return resolve_function(value)
    elif value.startswith('=='):
        value = value[1:]

    if value.isdigit():
        return (value, int(value))
    elif REAL.match(value):
        return (value, float(value))
    return (value, value)

def resolver_query(value):
    return value

def resolve_function(value):
    value = value[1:]
    dest = Invocation.gql("WHERE ihash = '%s'" % value).fetch(1)
    if not len(dest):
        raise Exception("Unable to resolve function invocation. Invocation hash: %s" % value)
    url = dest[0].url
    json = memcache.get(value)
    if not json:
        json = fetch(url).content
    return (url, loads(json)['value'])
