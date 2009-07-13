# -*- coding: utf-8 -*-
from urquell.http import Module
import test

lib = Module(None, 'lib')

def echo(*args, **kwargs):
    """echo can be used to test how *args and **kwargs will be presented
    to Python functions."""
    return {
        'arguments': args,
        'keywords': kwargs,
    }
lib.pure(test.echo, [
    '23/231.123123?hello=country&goodbye=nightclub',
    'hello%20country,%20goodbye%20nightclub',
])

def add(a, *b):
    """Add numbers"""
    for v in b:
        a = a + v
    return a
lib.pure(test.add, [
    '1/2',
])
def sub(a, *b):
    """Subtract one number from another"""
    for v in b:
        a = a - v
    return a
    return a - b
lib.pure(test.sub, [
    '2/1',
])
def mul(a, *b):
    """Multiply a set of numbers together"""
    for v in b:
        a = a * v
    return a
lib.pure(test.mul, [
    '2/1',
])
def div(a, *b):
    """Divide a set of numbers"""
    for v in b:
        a = a / v
    return a
lib.pure(test.div, [
    '2/3.0',
    '2/3.0/6',
])

def ifn(c, t, *f):
    if bool(c):
        return t
    else:
        return f
lib.pure(test.ifn, [])

def path_args(path):
    return '/'.join([quote(unicode(p)) for p in path])

def fn(server, *path):
    return "http://%s/%s" % (server, path_args(path))
lib.pure(test.fn, [
    'urquell-fn.appspot.com/lib/echo/',
    'urquell-fn.appspot.com/lib/add/1',
])
def bind(f, v):
    return "%s/%s" % (f, v)
lib.pure(test.bind, [
])
def call_trace(f, *path):
    from urquell import execute
    if len(path):
        return execute('%s/%s' % (f, path_args(path)))
    else:
        return execute(f)
lib.pure(test.call_trace, [])
def call(f, *path):
    return call_trace(f, *path)['value']
lib.pure(test.call, [])
