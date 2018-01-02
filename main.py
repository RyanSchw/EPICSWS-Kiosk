from google.appengine.api import users # Purpose?
import webapp2 # Used for class MainPage
import os # Purpose?
import datetime, time # Date/time library
import urllib, urllib2 # Something to do with REST requests
import json # Json formatting
import cgi # At the requrest of Python NDB
import textwrap # At the request of Python NDB

from google.appengine.ext.webapp import template # Purpose?
from google.appengine.ext import ndb # Import Python NDB client library


class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'title': "EPICS Weather Station"
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/', 'index.html')
        page = template.render(path, template_values)
        self.response.out.write(page)

class AdminPage(web,RequestHandler):
    def post(self):
        

# Says which things to execute when you hit each page
# Application will be just one page, except for diagnostics
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/json', AdminPage)
], debug=True)
