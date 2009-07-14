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
        if smodule:
            smodule.submodules.append(self)
        Responder.modules[self.path()] = self
        class Describe(webapp.RequestHandler):
            def get(describer):
                describer.response.out.write(template.render('urquell/templates/module.html', dict(
                    module = self,
                    description = description
                )))
        Responder.urls.append(('%s/$' % self.path(), Describe))
    def path(self):
        if self.supermodule:
            return "%s/%s" % (self.supermodule.path(), self.name)
        else:
            return "/%s" % self.name

    def pure(self, fn, examples = [], func_name=None):
        if func_name:
            fn.func_name = func_name
        self.functions.append(fn)
        module = self
        name = "%s/%s/.*" % (module.path(), fn.func_name)
        class Process(webapp.RequestHandler):
            def examples(self, exes):
                return template.render('urquell/templates/examples.html', dict(
                    module = module,
                    function = fn,
                    examples = exes
                ))
            def get(self):
                if self.request.path.endswith(".json"): # deprecated
                    invoke(self.request.path[:-5], self.request, module, fn)
                else:
                    json, obj = invoke(self.request.path, self.request, module, fn)
                    if self.request.headers.get('X-Requested-With', '').find('XMLHttpRequest') >= 0:
                        self.response.headers['Content-Type'] = 'text/plain'
                        self.response.out.write(json)
                    else:
                        self.response.out.write(template.render('urquell/templates/describe.html', dict(
                            result = obj,
                            value = dumps(obj.get('value', None)),
                            module = module,
                            function = fn,
                            examples = self.examples(examples)
                        )))
        Responder.urls.append((name, Process))
