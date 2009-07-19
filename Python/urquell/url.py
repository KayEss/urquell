# -*- coding: utf-8 -*-
import re, os, urllib, urlparse

class urlambda(object):
    def __init__(self, prefix, *path, **kwargs):
        parts = urlparse.urlsplit(prefix)
        self.prefix = '%s://%s/' % (parts[0], parts[1])
        self.path = parts[2][1:].split('/') + list(path)
        if len(self.path) == 1 and not self.path[0]:
            self.path = self.path[1:]
        self.kwargs = kwargs
