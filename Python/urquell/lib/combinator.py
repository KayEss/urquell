# -*- coding: utf-8 -*-
from urquell.http import Module
from urquell.lib import lib
from urquell.invocation import path_args


combinator = Module(lib, 'combinator', """Various combinators.""")


def I(v):
    """The identity combinator. This function can only take a single argument."""
    return v
combinator.pure(I, [
    '123',
    'hello%20world',
])
