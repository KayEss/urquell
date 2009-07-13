# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

from jsonrpc.json import dumps, loads

from urquell import Responder
from urquell.invocation import store_invocation, resolver_path, resolver_query


class Module(object):
    def __init__(self, smodule, name):
        self.supermodule = smodule
        self.name = name
        self.submodules = []
        self.functions = []
        if self.supermodule:
            self.supermodule.submodules.append(self)
        Responder.modules[self.path()] = self
        class Describe(webapp.RequestHandler):
            def get(describer):
                describer.response.out.write(template.render('urquell/templates/module.html', dict(
                    module = self
                )))
        Responder.urls.append(('%s/$' % self.path(), Describe))
    def path(self):
        if self.supermodule:
            return "%s/%s" % ( self.supermodule.path(), self.name )
        else:
            return "/%s" % self.name
    def describe(self, fn, exes):
        module = self
        name = "%s/%s.html" % (module.path(), fn.func_name)
        class Describe(webapp.RequestHandler):
            def examples(self, exes):
                return template.render('urquell/templates/examples.html', dict(
                    module = module,
                    function = fn,
                    examples = exes
                ))
            def get(self):
                self.response.out.write(template.render('urquell/templates/describe.html', dict(
                    module = module,
                    function = fn,
                    examples = self.examples(exes)
                )))
            def post(self):
                self.redirect('%s/%s.html' % (fn.func_name, self.request.POST['argument']))
        Responder.urls.append((name, Describe))
    def meta(self, fn, exes):
        name = "%s/%s.meta" % (self.path(), fn.func_name)
        class Meta(webapp.RequestHandler):
            def get(self):
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.out.write(dumps({
                    'name': fn.func_name,
                    'path': name,
                    'examples': exes,
                }))
        Responder.urls.append((name, Meta))
    def pure(self, fn, examples = []):
        self.functions.append(fn)
        self.describe(fn, examples)
        self.meta(fn, examples)
        module = self
        name = "%s/%s/.*" % (module.path(), fn.func_name)
        class Process(webapp.RequestHandler):
            def doapply(self, path):
                ihash = store_invocation(self.request.url)
                self.response.headers['Content-Type'] = 'text/plain'
                parts = path[len(module.path()) + len(fn.func_name) + 2:].split('/')
                call_trace = [resolver_path(str(i)) for i in parts]
                args = [x for u, x in call_trace]
                kwargs = dict(
                    [(str(k), resolver_query(self.request.GET[k])) for k in self.request.GET]
                )
                json = dumps({
                    'hash': u'=%s' % unicode(ihash),
                    'name': '%s/%s' % (module.path(), fn.func_name),
                    'args': [u for u, x in call_trace],
                    'path': path,
                    'value': fn(*args, **kwargs),
                })
                memcache.add(ihash, json, 300)
                self.response.out.write(json)
            def dobind(self, path):
                self.response.headers['Location'] = self.request.POST['argument']
            def get(self):
                if self.request.path.endswith(".json"): # deprecated
                    self.doapply(self.request.path[:-5])
                elif self.request.path.endswith(".bind"): # deprecated
                    self.dobind(self.request.path[:-5])
                else:
                    # TODO: Output should depend on headers
                    self.doapply(self.request.path)
        Responder.urls.append((name, Process))
