# -*- coding: utf-8 -*-
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from jsonrpc.json import dumps, loads
from urquell import Responder
import re, urllib

from google.appengine.api.urlfetch import fetch

REAL = re.compile('^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')
FUNCTION = re.compile('^=')
def resolver_path(value):
    value = urllib.unquote(value)
    if FUNCTION.match(value):
        return resolve_function(value)
    elif value.startswith('=='):
        value = value[1:]

    if value.isdigit():
        return (value, int(value))
    elif REAL.match(value):
        return (value, float(value))
    return (value, value)

def resolver_query(value):
    return value


def resolve_function(value):
    value = value[1:]
    url = 'http://bit.ly/%s' % value
    return (url, loads(fetch(url).content)['value'])


class Module(object):
    def __init__(self, smodule, name):
        self.supermodule = smodule
        self.name = name
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
                self.response.headers['Content-Type'] = 'text/html'
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
        self.describe(fn, examples)
        self.meta(fn, examples)
        module = self
        name = "%s/%s/.*" % (module.path(), fn.func_name)
        class Process(webapp.RequestHandler):
            def doapply(self, path):
                self.response.headers['Content-Type'] = 'text/plain'
                parts = path[len(module.path()) + len(fn.func_name) + 2:].split('/')
                call_trace = [resolver_path(str(i)) for i in parts]
                args = [x for u, x in call_trace]
                kwargs = dict(
                    [(str(k), resolver_query(self.request.GET[k])) for k in self.request.GET]
                )
                self.response.out.write(dumps({
                    'name': '%s/%s' % (module.path(), fn.func_name),
                    'args': [u for u, x in call_trace],
                    'path': path,
                    'value': fn(*args, **kwargs),
                }))
            def dobind(self, path):
                self.response.headers['Location'] = self.request.POST['argument']
            def get(self):
                if self.request.path.endswith(".json"):
                    self.doapply(self.request.path.rstrip(".json"))
                elif self.request.path.endswith(".bind"):
                    self.dobind(self.request.path.rstrip(".bind"))
                else:
                    self.response.headers['Content-Type'] = 'text/plain'
                    self.response.out.write(dumps("OK"))
        Responder.urls.append((name, Process))
