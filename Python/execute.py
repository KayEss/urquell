import wsgiref.handlers
from google.appengine.ext import webapp
from urquell import Responder
import urquell.lib


def main():
    application = webapp.WSGIApplication(Responder.urls, debug=True)
    wsgiref.handlers.CGIHandler().run(application)

