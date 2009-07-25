# -*- coding: utf-8 -*-
import urllib
from waveapi.simplejson import dumps, loads


def resolve_part(value):
    if value.startswith('**'):
        value = value[1:]
    elif value.startswith('*'):
        from invoke import resolve_hash
        return resolve_hash(value[1:])

    value = urllib.unquote(value)

    try:
        return (value, loads(value))
    except:
        return (value, value)


def unresolve_part(part):
    if type(part) == str or type(part) == unicode:
        if not len(part):
            return ''
        elif type(part) == str and part[0] != '*':
            return urllib.quote(part, '')
        else:
            return urllib.quote(dumps(part), '')
    else:
        return urllib.quote(dumps(part))
