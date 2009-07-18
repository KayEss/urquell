# -*- coding: utf-8 -*-
import wsgiref.handlers
from google.appengine.ext import webapp
from urquell.http import Responder

# These lines load the libraries and register the implementations
import urquell.lib.combinator
import urquell.lib.json
import urquell.lib.http

def main():
    application = webapp.WSGIApplication([('.*', Responder)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
