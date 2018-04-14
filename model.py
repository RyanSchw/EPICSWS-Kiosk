from datetime import datetime
from google.appengine.ext import ndb
import json

# Resource quotas for datastore (https://cloud.google.com/appengine/quotas?hl=en_US)
# Stored Data: 1 GB
# Number of Indexes: 200
# Entity Reads: 50,000
# Entity Writes: 20,000
# Entity Deletes: 20,000
# Small Operations: Unlimited

class LogButton(ndb.Model):
    time   = ndb.DateTimeProperty()
    button = ndb.StringProperty()

    @staticmethod
    def Insert(time, button):
        entry = LogButton(time=time, button=button)
        entry.put()

    @staticmethod
    def GetValues():
        q = LogButton.query()
        q = q.order(LogButton.time)
        return q.fetch()

    def RemoveAll():
        q = LogButton.query()
        ret = q.fetch()
        for entity in ret:
            entity.key.delete()

class Survey(ndb.Model):
    Q1 = ndb.IntegerProperty()
    Q2 = ndb.IntegerProperty()
    Q3 = ndb.IntegerProperty()

    @staticmethod
    def Insert(Q1, Q2, Q3):
        entry = Survey(Q1=Q1, Q2=Q2, Q3=Q3)
        entry.put()
