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

class WeatherStation(ndb.Model):
    time           = ndb.DateTimeProperty()
    wind_speed     = ndb.FloatProperty()
    wind_direction = ndb.StringProperty()
    wind_gust      = ndb.FloatProperty()
    rainfall       = ndb.FloatProperty()
    rainfall_rate  = ndb.FloatProperty()
    humidity       = ndb.FloatProperty()
    temperature    = ndb.FloatProperty()
    pressure       = ndb.FloatProperty()

    @staticmethod
    def Insert(time, wind_speed, wind_direction, wind_gust, rainfall, rainfall_rate, humidity, temperature, pressure):
        entry = WeatherStation(time=time,
                               wind_speed=wind_speed,
                               wind_direction=wind_direction,
                               wind_gust=wind_gust,
                               rainfall=rainfall,
                               rainfall_rate=rainfall_rate,
                               humidity=humidity,
                               temperature=temperature,
                               pressure=pressure)
        entry.put()

    @staticmethod
    def GetValues():
        q = WeatherStation.query()
        q = q.order(WeatherStation.time)
        return q.fetch()




class Cities(ndb.Model):
    city           = ndb.StringProperty()
    time           = ndb.DateTimeProperty()
    wind_speed     = ndb.FloatProperty()
    wind_direction = ndb.StringProperty()
    wind_gust      = ndb.FloatProperty()
    rainfall       = ndb.FloatProperty()
    humidity       = ndb.FloatProperty()
    temperature    = ndb.FloatProperty()
    pressure       = ndb.FloatProperty()

    @classmethod
    def Insert(cls, city, time, wind_speed, wind_direction, wind_gust, rainfall, humidity, temperature, pressure):
        print "INSERT REQUEST " + city
        entry = Cities(city=city,
                       time=time,
                       wind_speed=wind_speed,
                       wind_direction=wind_direction,
                       wind_gust=wind_gust,
                       rainfall=rainfall,
                       humidity=humidity,
                       temperature=temperature,
                       pressure=pressure)
        entry.put()

    @staticmethod
    def GetValues(cityParam):
        q = Cities.query(Cities.city == cityParam)
        # Newest first
        q = q.order(Cities.time)
        return q.fetch()

    @staticmethod
    def RemoveOldestValue():
        q = Cities.query()
        # Oldest first
        q = q.order(Cities.time)
        ret = q.fetch(1)
        for entity in ret:
            entity.key.delete()
            return entity
