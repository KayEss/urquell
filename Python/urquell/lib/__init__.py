# -*- coding: utf-8 -*-
from urquell.http import Module
from urquell.invocation import path_args
import test

lib = Module(None, 'lib', """A general purpose library providing a number of useful functions.""")

def echo(*args, **kwargs):
    """echo can be used to test how *args and **kwargs will be presented
    to Python functions."""
    return {
        'arguments': args,
        'keywords': kwargs,
    }
lib.pure(echo, [
    '23/231.123123?hello=country&goodbye=nightclub',
    'hello%20country,%20goodbye%20nightclub',
])

def add(a, *b):
    """Add numbers"""
    for v in b:
        a = a + v
    return a
lib.pure(add, [
    '1/2',
    '1/2/3/4',
])
def sub(a, *b):
    """Subtract one number from another"""
    for v in b:
        a = a - v
    return a
    return a - b
lib.pure(sub, [
    '2/1',
    '2/1/-1',
])
def mul(a, *b):
    """Multiply a set of numbers together"""
    for v in b:
        a = a * v
    return a
lib.pure(mul, [
    '2/1',
])
def div(a, *b):
    """Divide a set of numbers"""
    for v in b:
        a = a / v
    return a
lib.pure(div, [
    '2/3.0',
    '2/3.0/6',
])

def ift(c, t = None, *f):
    """A conditional which returns its first argument if the condition is met, otherwise it returns all the other arguments."""
    if bool(c):
        return t
    else:
        return f
lib.pure(ift, [
], func_name = "if")


def fn(server, *path):
    """Constructs a function from a server name and a path."""
    return "http://%s/%s" % (server, path_args(path))
lib.pure(fn, [
    'urquell-fn.appspot.com/lib/echo/',
    'urquell-fn.appspot.com/lib/echo/hello/%20/world',
    'urquell-fn.appspot.com/lib/add/1',
])
def bind(f, *path):
    """Binds arguments to a function."""
    if f and len(path):
        return "%s/%s" % (f, path_args(path))
    elif f:
        return f
    else:
        return None
lib.pure(bind, [
])
def call_trace(f, *path):
    """Execute a function and return all of the debugging information."""
    from urquell.invocation import execute
    if len(path):
        return execute('%s/%s' % (f, path_args(path)))
    else:
        return execute(f)
lib.pure(call_trace, [])
def call(f, *path):
    """Execute a function returning just the function's return value."""
    return (call_trace(f, *path) or {}).get('value', None)
lib.pure(call, [])
