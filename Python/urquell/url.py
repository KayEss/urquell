# -*- coding: utf-8 -*-
import re, os, urllib, urlparse

class urlambda(object):
    def __init__(self, prefix, *path, **kwargs):
        parts = urlparse.urlsplit(prefix)
        # Prefix is easy
        self.prefix = '%s://%s/' % (parts[0], parts[1])
        # The path needs to be appended in the right way
        self.path = parts[2][1:].split('/')
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
        return self.prefix

    def __eq__(self, other):
        return self.prefix == other.prefix and self.path == other.path and self.state == other.state
