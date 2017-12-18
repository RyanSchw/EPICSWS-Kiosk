from google.appengine.api import users
import webapp2
import os
import datetime, time
import urllib, urllib2
import json
from google.appengine.ext.webapp import template


class MainPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'title': "EPICS Weather Station"
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/', 'index.html')
        page = template.render(path, template_values)
        self.response.out.write(page)

# Email stuff


# Says which things to execute when you hit each page
application = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
