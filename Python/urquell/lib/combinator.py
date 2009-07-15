# -*- coding: utf-8 -*-
from urquell.http import Module, Function
from urquell.lib import lib, call
from urquell.invocation import path_args


combinator = Module(lib, 'combinator', """Various combinators. All of the combinators throw away key word arguments.""")


def I(v, *p, **k):
    """
        <p>The identity combinator.</p>
        <p>This version of the identity combinator cannot work with both path arguments and query string arguments. If there is any path element at all then the query string is discarded. If the path is empty then the query string is returned as a JSON object.</p>
    """
    if not v and not len(p):
        return k
    elif len(p):
        return [v] + list(p)
    else:
        return v
Function(combinator, I, [
    '123',
    'hello%20world',
    'hello/world',
    '?hello=world',
    'hello/world?hello=world',
])

def K(f, *z, **kw):
    """
        <p>The K combinator. This is also known as the Kestrel.</p>
        <p>K takes a function (resolved through a bind expression which will have been created via something like <a href="/lib/fn/">lib/fn</a>), executes the function over its other inputs and then returns the original function.</p>
    """
    call(f, *z, **kw)
    return f
Function(combinator, K, [
])

def S(*v):
    """
        <p>The S combinator.</p>
    """
