# -*- coding: utf-8 -*-
from urquell.http import Module, Function, root
from urquell.value import path_args
from jsonrpc.json import dumps
import urllib

lib = Module(root, 'lib', """
    <p>A general purpose library providing a number of useful functions.</p>
""")

def echo(*args, **kwargs):
    """
        <p>echo can be used to test how *args and **kwargs will be presented
    to Python functions.</p>
    """
    return {
        'arguments': args,
        'keywords': kwargs,
    }
Function(lib, echo, [
    '23/231.123123?hello=country&goodbye=nightclub',
    'hello%20country,%20goodbye%20nightclub',
])

def add(a, *b, **kw):
    """Add numbers"""
    for v in b:
        a = a + v
    return a
Function(lib, add, [
    '1/2',
    '1/2/3/4',
])
def sub(a, *b, **kw):
    """Subtract one number from another"""
    for v in b:
        a = a - v
    return a
Function(lib, sub, [
    '2/1',
    '2/1/-1',
])
def mul(a, *b, **kw):
    """Multiply a set of numbers together"""
    for v in b:
        a = a * v
    return a
Function(lib, mul, [
    '2/1',
])
def div(a, *b, **kw):
    """Divide a set of numbers"""
    for v in b:
        a = a / v
    return a
Function(lib, div, [
    '2/3.0',
    '2/3.0/6',
])

def ift(c, t, *f, **kw):
    """
        <p>A conditional which returns its first argument if the condition is met, otherwise it returns all the other arguments.</p>
    """
    if bool(c):
        return t
    else:
        return f
Function(lib, ift, [
], func_name = "if")


def throw(message, *args, **kwargs):
    """
        <p>Raises an exception with the first argument as the main exception text also giving it a JSON representation of the arguments and kwargs</p>
    """
    try:
        json = dumps({'args':args, 'kwargs':kwargs})
    except Exception, e:
        raise Exception('%s\nError generating JSON: %s' % (message, e))
    raise Exception('%s\n%s' % (message, json))
Function(lib, throw, [
])

def fn(server, *path, **kw):
    """
        <p>Constructs a function from a server name and a path.</p>
    """
    return "http://%s/%s" % (server, path_args(path))
Function(lib, fn, [
    'urquell-fn.appspot.com/lib/echo/',
    'urquell-fn.appspot.com/lib/echo/hello/%20/world',
    'urquell-fn.appspot.com/lib/add/1',
])
def bind(f, *path, **kwargs):
    """
        <p>Binds an argument list to a function. Optionally, values can also be
        bound to those arguments using the query string. When the argument list
        is left unbound, values can later be applied using functions such as
        lib/call and lib/combinator/K.</p>
    """
    if f and len(path):
        for p in path:
            v = urllib.quote(kwargs.get(p, '*'), '')
            if f[-1] == '/':
                f = '%s%s' % (f, v)
            else:
                f = '%s/%s' % (f, v)
        return f
    elif f:
        return f
    else:
        return None
Function(lib, bind, [
    '*2wuQZl_G/a/b/c',
    '*-UvxBuFm/a/b/c?a=1&b=2&c=3'
])
def call_trace(f, *path, **kwargs):
    """
        <p>Execute a function and return all of the debugging information.</p>
    """
    from urquell.invocation import ErrorTrace, execute
    query_string = '&'.join(['%s=%s' % (urllib.quote(k, '*/'), urllib.quote(v, '*/')) for k, v in kwargs.items()])
    if len(path):
        if f[-1] == '/':
            f = '%s%s' % (f, path_args(path))
        else:
            f = '%s/%s' % (f, path_args(path))
    if query_string:
        return execute('%s?%s' % (f, query_string))
    else:
        return execute(f)
Function(lib, call_trace, [
    '*LsRUxMs0/Hello%20world',
    '*N698-V54/lib',
])
def call(f, *path, **kwargs):
    """
        <p>Execute a function returning just the function's return value.</p>
    """
    from urquell.invocation import ErrorTrace
    inner = call_trace(f, *path, **kwargs)
    if not inner.has_key('value'):
        raise ErrorTrace("Function invocation failed", inner)
    return inner['value']
Function(lib, call, [
    '*LsRUxMs0/Hello%20world',
    '*N698-V54/lib/http',
])

def unresolve(c):
    """
        <p>Takes a binding code and returns the lambda associated with it. Binding code literals need to be without a leading star.</p>
    """
    from urquell.invocation import retrieve_invocation
    return retrieve_invocation(c)
Function(lib, unresolve, [
    'LsRUxMs0',
    'N698-V54',
])

def map(f, *path, **kw):
    """
        <p>Execute the same function across all of the remaining inputs.</p>
    """
    from urquell.invocation import execute
    return [execute('%s/%s' % (f, p))['value'] for p in path]
Function(lib, map, [
])
