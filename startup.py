# Handles initial startup of server
from requests import WeatherUnderground as WU
import time
import webapp2

class start(webapp2.RequestHandler):
    def get(self):
        WU.updateData()
        for x in range(0, 5):
            WU.verifyData()
            time.sleep(60)
