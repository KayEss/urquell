# -*- coding: utf-8 -*-
from urquell.http import Module
import test

lib = Module(None, 'lib')

lib.pure(test.echo, [
    '23/231.123123.json?hello=country&goodbye=nightclub',
    'hello%20country,%20goodbye%20nightclub',
])

lib.pure(test.add, [
    '1/2.json'
])
lib.pure(test.sub, [
    '2/1.json'
])
lib.pure(test.mul, [
    '2/1.json'
])

lib.pure(test.ifn, [])

lib.pure(test.fn, [])
lib.pure(test.bind, [])
lib.pure(test.call_trace, [])
lib.pure(test.call, [])
