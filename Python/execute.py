# -*- coding: utf-8 -*-
import wsgiref.handlers
from google.appengine.ext import webapp
from urquell import Responder

import urquell.lib.http

def main():
    application = webapp.WSGIApplication(Responder.urls, debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()
