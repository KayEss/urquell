# -*- coding: utf-8 -*-
import re, os, urllib, urlparse
from value import resolve_part


class urlambda(object):
    def __init__(self, prefix, *path, **kwargs):
        parts = urlparse.urlsplit(prefix)
        # Prefix is easy
        self.prefix = '%s://%s/' % (parts[0], parts[1])
        # The path needs to be appended in the right way
        self.path = [resolve_part(p)[0] for p in parts[2][1:].split('/')]
        if len(self.path) == 1 and not self.path[0]:
            self.path = self.path[1:]
        self.path += list(path)
        # We have to parse the query string
        self.state = {}
        if parts[3]:
            for kv in parts[3].split('&'):
                key, eq, value = kv.partition('=')
                if not self.state.has_key(key):
                    self.state[key] = value
                elif hasattr(self.state[key], 'append'):
                    self.state[key].append(value)
                else:
                    self.state[key] = [self.state[key], value]
        for k, v in kwargs.items():
            self.state[k] = v

    def __repr__(self):
        def pathize(i):
            if str(i) == i and len(i) and i[0] != '*':
                return urllib.quote(str(i))
            else:
                return urllib.quote(unicode(i))
        path = '/'.join([pathize(p) for p in self.path])
        return self.prefix + path

    def __eq__(self, other):
        return self.prefix == other.prefix and self.path == other.path and self.state == other.state
