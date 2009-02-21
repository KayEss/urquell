from google.appengine.ext import webapp
from jsonrpc.json import dumps, loads
from urquell import Responder
import re


REAL = re.compile('^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')
def resolver_path(value):
    if value.isdigit():
        return int(value)
    elif REAL.match(value):
        return float(value)
    return value

def resolver_query(value):
    return value


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
                lis = ""
                for ex in exes:
                    lis = '%s<li><a href="%s/%s">%s/%s/%s</a></li>' % (
                        lis, fn.func_name, ex, module.path(), fn.func_name, ex
                    )
                if len(lis):
                    return "<ol>%s</ol>" % lis
                else:
                    return ""
            def get(self):
                self.response.headers['Content-Type'] = 'text/html'
                self.response.out.write("""<html>
                    <head><title>%s</title></head>
                    <body>
                        <h1>%s</h1>%s
                        <h2>Examples</h1>%s
                    </body>
                </html>""" % (
                    fn.func_name, fn.func_name, fn.func_doc, self.examples(exes))
                )
        Responder.urls.append((name, Describe))
    def meta(self, fn, exes):
        module = self
        name = "%s/%s.meta" % (module.path(), fn.func_name)
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
                parts = path.strip(name).split('/')
                args = []
                for i in parts:
                    args.append(resolver_path(str(i)))
                kwargs = {}
                for k in self.request.GET:
                    kwargs[str(k)] = resolver_query(self.request.GET[k])
                self.response.out.write(dumps(fn(*args, **kwargs)))
            def get(self):
                if self.request.path.endswith(".json"):
                    self.doapply(self.request.path.rstrip(".json"))
                else:
                    self.response.headers['Content-Type'] = 'text/plain'
                    self.response.out.write(dumps("OK"))
        Responder.urls.append((name, Process))