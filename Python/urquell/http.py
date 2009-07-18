# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from jsonrpc.json import dumps, loads

from urquell import Responder
from urquell.invocation import invoke, store_invocation, resolver_path, resolver_query


class Module(object):
    def __init__(self, smodule, name, description = None):
        self.supermodule = smodule
        self.name = name
        self.submodules = []
        self.functions = []
        self.description = description
        if smodule:
            smodule.submodules.append(self)
        else:
            Responder.modules.append(self)

    def path(self):
        if self.supermodule:
            return "%s/%s" % (self.supermodule.path(), self.name)
        else:
            return "/%s" % self.name

    def resolve(self, path):
        if not path:
            return self
        else:
            for m in self.submodules + self.functions:
                if path.startswith('%s/' % m.name):
                    return m.resolve(path[len(m.name)+1:])

    def get(self, request):
        return template.render('urquell/templates/module.html', dict(
            module = self,
            description = self.description
        )), None, 200

class Function(object):
    def __init__(self, module, fn, examples = [], func_name=None):
        if func_name:
            fn.func_name = func_name
        self.module = module
        self.fn = fn
        self.name = func_name or fn.func_name
        self.examples = examples
        self.module.functions.append(self)

    def resolve(self, path):
        return self

    def get(self, request):
        json, obj = invoke(request.path, request, self.module, self.fn)
        if obj.has_key('error'):
            status = 500
        else:
            status = 200
        if request.headers.get('X-Requested-With', '').find('XMLHttpRequest') >= 0:
            return json, 'text/plain', status
        else:
            return template.render('urquell/templates/describe.html', dict(
                result = obj,
                value = dumps(obj.get('value', None)),
                error = obj.get('error', None),
                module = self.module,
                function = self.fn,
                examples = template.render('urquell/templates/examples.html', dict(
                    module = self.module,
                    function = self.fn,
                    examples = self.examples
                )),
            )), None, status
