import urllib2
import json
import webapp2
import os
import logging

from google.appengine.ext import ndb
from datetime import datetime
import datetime as td

import API_Keys as keys
from model import LogButton
from model import Survey
from custom_email import EmailRequest

#########################################################
###                                                   ###
###       Handles all incoming service requests       ###
###                                                   ###
#########################################################


# When client tells us stuff is wrong
class ErrorInput(webapp2.RequestHandler):
    def post(self):
        message = self.request.POST.get('message')
        EmailRequest.serviceRequest(message)
        self.response.out.write("Message received by server.")


class Submit(webapp2.RequestHandler):
    def post(self):
        LogButton.Insert(datetime.utcfromtimestamp(float(self.request.POST.get('time'))), self.request.POST.get('button'))


class Stats(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(LogButton.GetValues())

class SubmitSurvey(webapp2.RequestHandler):
    def post(self):
        Survey.Insert(int(self.request.POST.get('Q1')), int(self.request.POST.get('Q2')), int(self.request.POST.get('Q3')))


class Data(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        dummydata = ''' {
           "Sacramento":{
              "wind_gust":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "wind_gust":0.0
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "wind_gust":0.0
                 }
              ],
              "rainfall":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "rainfall":0.0
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "rainfall":0.0
                 }
              ],
              "pressure":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "pressure":30.14
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "pressure":31.0
                 }
              ],
              "temperature":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "temperature":65.3
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "temperature":65.8
                 }
              ],
              "wind_direction":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "wind_direction":"SSE"
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "wind_direction":"SSE"
                 }
              ],
              "wind_speed":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "wind_speed":0.0
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "wind_speed":0.0
                 }
              ],
              "humidity":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "humidity":59.0
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "humidity":60.0
                 }
              ]
           },
           "Washington":{
              "wind_gust":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "wind_gust":0.0
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "wind_gust":0.0
                 }
              ],
              "rainfall":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "rainfall":0.0
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "rainfall":0.0
                 }
              ],
              "pressure":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "pressure":30.22
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "pressure":30.04
                 }
              ],
              "temperature":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "temperature":41.9
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "temperature":42.1
                 }
              ],
              "wind_direction":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "wind_direction":"SW"
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "wind_direction":"SW"
                 }
              ],
              "wind_speed":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "wind_speed":0.0
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "wind_speed":0.0
                 }
              ],
              "humidity":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "humidity":92.0
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "humidity":92.2
                 }
              ]
           },
           "Weather Station":{
              "wind_gust":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "wind_gust":0.0
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "wind_gust":0.0
                 }
              ],
              "rainfall":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "rainfall":0.0
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "rainfall":0.0
                 }
              ],
              "pressure":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "pressure":30.22
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "pressure":30.04
                 }
              ],
              "temperature":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "temperature":41.9
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "temperature":42.1
                 }
              ],
              "wind_direction":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "wind_direction":"SW"
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "wind_direction":"SW"
                 }
              ],
              "wind_speed":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "wind_speed":0.0
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "wind_speed":0.0
                 }
              ],
              "humidity":[
                 {
                    "time":"2018-03-28T04:41:32",
                    "humidity":92.0
                 },
                 {
                    "time":"2018-03-28T05:41:32",
                    "humidity":92.2
                 }
              ]
           },
           "Tampa":{
              "wind_gust":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "wind_gust":11.0
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "wind_gust":2.0
                 }
              ],
              "rainfall":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "rainfall":0.0
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "rainfall":0.0
                 }
              ],
              "pressure":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "pressure":30.26
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "pressure":30.01
                 }
              ],
              "temperature":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "temperature":65.8
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "temperature":66.3
                 }
              ],
              "wind_direction":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "wind_direction":"SE"
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "wind_direction":"SE"
                 }
              ],
              "wind_speed":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "wind_speed":11.0
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "wind_speed":4.0
                 }
              ],
              "humidity":[
                 {
                    "time":"2018-03-28T04:41:29",
                    "humidity":66.0
                 },
                 {
                    "time":"2018-03-28T05:41:29",
                    "humidity":66.5
                 }
              ]
           }
        } '''

        self.response.out.write(dummydata)
