# -*- coding: utf-8 -*-
from urllib import quote
from urquell import execute


def echo(*args, **kwargs):
    """echo can be used to test how *args and **kwargs will be presented
    to Python functions."""
    return {
        'arguments': args,
        'keywords': kwargs,
    }


def add(a, *b):
    """Add numbers"""
    for v in b:
        a = a + v
    return a
def sub(a, b):
    """Subtract one number from another"""
    return a - b
def mul(a, b):
    return a * b


def ifn(c, t, f):
    if bool(c):
        return t
    else:
        return f


def path_args(path):
    return '/'.join([quote(unicode(p)) for p in path])

def fn(server, *path):
    return "http://%s/%s" % (server, path_args(path))
def bind(f, v):
    return "%s/%s" % (f, v)
def call_trace(f, *path):
    return {'value': (f, path)}
def call(f, *path):
    return call_trace(f, *path)['value']
