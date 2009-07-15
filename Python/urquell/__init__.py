# -*- coding: utf-8 -*-
from jsonrpc.json import dumps, loads
from google.appengine.ext import webapp
from google.appengine.api.urlfetch import fetch
from google.appengine.ext.webapp import template


class Homepage(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('urquell/templates/homepage.html', dict(
            modules = Responder.modules
        )))

class Responder(webapp.RequestHandler):
    modules = []

    def hit(self, path):
        for m in self.modules:
            if path.startswith('/%s/' % m.name):
                return m.resolve(path[len(m.name)+2:])
            elif path == '/%s' % m.name:
                pass

    def get(self):
        hit = self.hit(self.request.path)
        response, mime = hit.get(self.request)
        if mime:
            self.response.headers['Content-Type'] = mime
        self.response.out.write(response)

urls = [
    ('^/$', Homepage),
    ('.*', Responder)
]
