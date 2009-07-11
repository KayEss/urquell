# -*- coding: utf-8 -*-
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


def fn(server, *path):
    return "http://%s/%s" % (server, '/'.join(path))
def bind(f, v):
    return "%s/%s" % (f, v)
def call_trace(f):
    return execute("%s.json"%f)
def call(f):
    return call_trace(f)['value']
