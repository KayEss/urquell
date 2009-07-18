# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from jsonrpc.json import dumps, loads

from urquell.invocation import invoke, store_invocation


class Responder(webapp.RequestHandler):
    def get(self):
        path = self.request.path.split('/')
        response, mime, status = root.get(self, *path)
        self.response.set_status(status)
        if mime:
            self.response.headers['Content-Type'] = mime
        self.response.out.write(response)

class EndPoint(object):
    """
        This class acts as the root of the Urquell namespace and is placed into the root of the web site. It is responsible for routing the request to the correct function depending on the path contents.
    """
    def __init__(self, name, description):
        super(EndPoint, self).__init__()
        self.name = name
        self.description = description
        self.routes = {}

    def path(self):
        return ''
    def do404(self, responder):
        return template.render('urquell/templates/404.html', dict(
            path = responder.request.path
        )), None, 404
    def route(self, responder, *path, **kwargs):
        name, path = path[0], path[1:]
        function = self.routes.get(name, None)
        if not function:
            return self.do404(responder)
        return function.get(responder, *path, **kwargs)
    def get(self, responder, *path, **kwargs):
        if len(path):
            return self.route(responder, *path, **kwargs)
        return template.render('urquell/templates/homepage.html', dict(
            modules = self.routes
        )), None, 200

root = EndPoint(None, None)
root.routes[''] = root


class Contained(EndPoint):
    def __init__(self, container, name, description):
        super(Contained, self).__init__(name, description)
        self.container = container
        self.container.routes[self.name] = self

    def path(self):
        return "%s/%s" % (self.container.path(), self.name)

class Module(Contained):
    def __init__(self, smodule, name, description):
        super(Module, self).__init__(smodule, name, description)
        self.submodules = []
        self.functions = []
        if hasattr(self.container, 'submodules'):
            self.container.submodules.append(self)

    def get(self, request, *path, **kwargs):
        if not len(path):
            return template.render('urquell/templates/module.html', dict(
                module = self,
                description = self.description
            )), None, 200
        return self.route(request, *path, **kwargs)

class Function(Contained):
    def __init__(self, module, fn, examples = [], func_name = None, func_doc = None):
        super(Function, self).__init__(module, func_name or fn.func_name, func_doc or fn.func_doc)
        self.container.functions.append(self)
        self.fn = fn
        self.examples = examples

    def path(self):
        return "%s/%s" % (self.container.path(), self.name)

    def describe(self, json, obj, status):
        return template.render('urquell/templates/describe.html', dict(
            result = obj,
            value = dumps(obj.get('value', None)),
            error = obj.get('error', None),
            module = self.container,
            function = self,
            examples = template.render('urquell/templates/examples.html', dict(
                module = self.container,
                function = self.fn,
                examples = self.examples
            )),
        )), None, status

    def get(self, responder, *path, **kwargs):
        json, obj = invoke(responder.request.path, responder.request, self.container, self.fn)
        if obj.has_key('error'):
            status = 500
        else:
            status = 200
        if responder.request.headers.get('X-Requested-With', '').find('XMLHttpRequest') >= 0:
            return json, 'text/plain', status
        else:
            return self.describe(json, obj, status)
