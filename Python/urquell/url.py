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
        self.state = parts[3] or {}

