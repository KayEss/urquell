# -*- coding: utf-8 -*-
import re, os, urllib
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api.urlfetch import fetch

from waveapi.simplejson import dumps, loads

from urquell.invocation import ErrorTrace, Invocation, execute


REAL = re.compile('^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')
FUNCTION = re.compile('^=')
def resolve_part(value):
    value = urllib.unquote(value)
    if value.startswith('**'):
        value = value[1:]
    elif value.startswith('*'):
        return resolve_hash(value[1:])

    if value.isdigit():
        return (value, int(value))
    elif REAL.match(value):
        return (value, float(value))
    return (value, value)

def resolve_hash(value):
    dest = Invocation.gql("WHERE ihash = :1", value).fetch(1)
    if not len(dest):
        raise ErrorTrace("Unable to resolve function invocation. Invocation hash: %s" % value)
    url = dest[0].url
    json = memcache.get(value)
    if not json:
        rvalue = execute(url)
    else:
        rvalue = loads(json)
    if rvalue.has_key('value'):
        return url, rvalue['value']
    else:
        raise ErrorTrace("Whilst resolving binding value %s" % value, rvalue)

def path_args(path):
    return '/'.join([urllib.quote(unicode(p), '') for p in path])
