# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from waveapi.simplejson import dumps, loads

from urquell.invocation import ErrorTrace, invoke, store_invocation
from urquell.value import resolve_part


class Responder(webapp.RequestHandler):
    def get(self):
        self.object = {
            'path': self.request.path,
            'headers': dict([(k, unicode(v)) for k, v in self.request.headers.items()]),
        }
        self.template = 'urquell/templates/function.html'
        self.context = {}
        self.status = 200
        try:
            path = [resolve_part(str(i))[1] for i in self.request.path[1:].split('/')]
            kwargs = dict([(str(resolve_part(k)[1]), resolve_part(v)[1]) for k, v in self.request.GET.items()])
            root.get(self, *path, **kwargs)
        except ErrorTrace, e:
            self.status = 500
            self.object['error'] = {
                'message': e.message,
                'trace': e.trace
            }
        except Exception, e:
            import traceback
            self.status = 500
            self.object['error'] = {
                'message': unicode(e),
                'python': {
                    'call_trace': traceback.format_exc(),
                },
            }
        self.response.set_status(self.status)
        if self.request.headers.get('X-Requested-With', '').find('XMLHttpRequest') >= 0 or self.request.GET.has_key('__'):
            self.response.headers['Content-Type'] = 'text/plain'
            text = dumps(self.object)
            if self.request.GET.get('__', None):
                self.response.out.write("%s(%s);" % (self.request.GET['__'], text))
            else:
                self.response.out.write(text)
        else:
            self.context['result'] = self.object
            self.context['status'] = self.status
            if self.object.has_key('value'):
                self.context['value'] = dumps(self.object['value'])
            self.context['error'] = self.object.get('error', None)
            self.response.out.write(template.render(self.template, self.context))


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
    def do404(self, responder, requested = None):
        responder.object['error'] = {
            'message': "Urquell function or module not found",
            "options": self.routes.keys(),
        }
        if requested:
            responder.object['error']['requested'] = requested
        responder.status = 404
        responder.template = 'urquell/templates/404.html'
        responder.context = dict(
            path = responder.request.path
        )
    def route(self, responder, *path, **kwargs):
        name, path = path[0], path[1:]
        function = self.routes.get(name, None)
        if not function:
            self.do404(responder, name)
        else:
            function.get(responder, *path, **kwargs)
    def get(self, responder, *path, **kwargs):
        if len(path) == 1 and not path[0]:
            responder.object['value'] = {
                "modules": [{
                    'name': m.name,
                } for k, m in self.routes.items()],
            }
            responder.template = 'urquell/templates/homepage.html'
            responder.context = dict(
                modules = self.routes
            )
        else:
            self.route(responder, *path, **kwargs)

root = EndPoint(None, None)


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

    def get(self, responder, *path, **kwargs):
        if not len(path):
            responder.object['value'] = {
                'modules': [{
                    'name': m.name,
                } for m in self.submodules],
                'functions': [{
                    'name': f.name,
                } for f in self.functions],
            }
            responder.template = 'urquell/templates/module.html'
            responder.context = dict(
                module = self,
                description = self.description,
            )
        else:
            self.route(responder, *path, **kwargs)

class Function(Contained):
    def __init__(self, module, fn, examples = [], func_name = None, func_doc = None):
        super(Function, self).__init__(module, func_name or fn.func_name, func_doc or fn.func_doc)
        self.container.functions.append(self)
        self.fn = fn
        self.examples = examples

    def get(self, responder, *path, **kwargs):
        responder.context['function'] = self
        invoke(responder, self.container, self.fn, *path, **kwargs)
