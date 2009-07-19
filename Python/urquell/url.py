# -*- coding: utf-8 -*-
import re, os, urllib, urlparse

class urlambda(object):
    def __init__(self, prefix, *path, **kwargs):
        parts = urlparse.urlsplit(prefix)
        self.prefix = '%s://%s/' % (parts[0], parts[1])
        self.path = path
        self.kwargs = kwargs

