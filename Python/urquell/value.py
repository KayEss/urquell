# -*- coding: utf-8 -*-
import re, os, urllib

from waveapi.simplejson import dumps, loads


REAL = re.compile('^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')

def resolve_part(value):
    if value.startswith('**'):
        value = value[1:]
    elif value.startswith('*'):
        return resolve_hash(value[1:])

    value = urllib.unquote(value)

    if value.isdigit():
        return (value, int(value))
    elif REAL.match(value):
        return (value, float(value))
    return (value, value)
