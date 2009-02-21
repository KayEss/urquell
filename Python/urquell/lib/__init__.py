from urquell.http import Module
import test

lib = Module(None, 'lib')
lib.pure(test.echo, [
    '23/231.123123/.json?hello=country&goodbye=nightclub',
    'hello%20country,%20goodbye%20nightclub',
])
