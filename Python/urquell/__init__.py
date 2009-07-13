# -*- coding: utf-8 -*-
from jsonrpc.json import dumps, loads
from google.appengine.ext import webapp
from google.appengine.api.urlfetch import fetch
from google.appengine.ext.webapp import template


class Homepage(webapp.RequestHandler):
    def get(self):
        self.response.out.write(template.render('urquell/templates/homepage.html', dict(
            modules = Responder.modules.values()
        )))

class Responder(object):
    urls = [('^/$', Homepage)]
    modules = {}
