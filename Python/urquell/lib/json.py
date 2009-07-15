# -*- coding: utf-8 -*-
from urquell.http import Module, Function
from urquell.lib import lib


json = Module(lib, 'json', """
    <p>JSON creation and manipulation functions.<p>
""")


def object(*keys, **values):
    """
        <p>Constructs a JSON object from the specified keys. Values can be passed as the query string.</p>
    """
    o = {}
    if len(keys) > 1 and keys[0]:
        for k in keys:
            o[k] = None
    for k, v in values.items():
        o[k] = v
    return o
Function(json, object, [
    '',
    'key',
    'key1/key2',
    'key1/key2?key1=45&key2=Hello+world',
    '?key1=45&key2=Hello+world'
])

def array(*path):
    """
        <p>Constructs a JSON array from the path elements.</p>
    """
    if len(path) == 1 and not path[0]:
        return []
    return path
Function(json, array, [
    '',
    '1',
    '1/2/3',
])
