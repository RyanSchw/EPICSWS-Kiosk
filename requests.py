import urllib2
import json
import webapp2

from google.appengine.ext import ndb
from datetime import datetime
import datetime as td

import API_Keys as keys
from model import WeatherStation
from model import Cities
from custom_email import EmailRequest

#########################################################
###                                                   ###
###       Handles all incoming service requests       ###
###                                                   ###
#########################################################

# Formats JSON data to be returned to browser; last step in returning process
# Also formats WS emails to be sent to GLOBE
class Formatter:
    @staticmethod
    def formatTime(unf):
        return unf.isoformat()

    @staticmethod
    def formatWU(wu, ws):
        result = {}
        wspd = []
        wd = []
        wg = []
        r = []
        h = []
        t = []
        p = []
        for city in wu:
            for entity in city:
                current_city = entity.city
                time = Formatter.formatTime(entity.time)
                wspd.append({'time': time, 'wind_speed': entity.wind_speed})
                wd.append({'time': time, 'wind_direction': entity.wind_direction})
                wg.append({'time': time, 'wind_gust': entity.wind_gust})
                r.append({'time': time, 'rainfall': entity.rainfall})
                h.append({'time': time, 'humidity': entity.humidity})
                t.append({'time': time, 'temperature': entity.temperature})
                p.append({'time': time, 'pressure': entity.pressure})
            result[current_city] = {"wind_speed": wspd,
                                    "wind_direction": wd,
                                    "wind_gust": wg,
                                    "rainfall": r,
                                    "humidity": h,
                                    "temperature": t,
                                    "pressure": p}
            wspd = []
            wd = []
            wg = []
            r = []
            h = []
            t = []
            p = []
        for entity in ws:
            wspd.append({'time': time, 'wind_speed': entity.wind_speed})
            wd.append({'time': time, 'wind_direction': entity.wind_direction})
            wg.append({'time': time, 'wind_gust': entity.wind_gust})
            r.append({'time': time, 'rainfall': entity.rainfall})
            h.append({'time': time, 'humidity': entity.humidity})
            t.append({'time': time, 'temperature': entity.temperature})
            p.append({'time': time, 'pressure': entity.pressure})
        result["Weather Station"] = {"wind_speed": wspd,
                                "wind_direction": wd,
                                "wind_gust": wg,
                                "rainfall": r,
                                "humidity": h,
                                "temperature": t,
                                "pressure": p}
        return json.dumps(result, separators=(',', ':'))

    @staticmethod
    def formatWS(unformatted):
        body = ""
        for entry in unformatted:
            # Everything has accuracy to two decimal points, adjust as needed
            tempc = float(entry.temperature - 32) * float(5 / 9)
            body += "DAVAD " + keys.SCHOOL_ID + " " + keys.SITE_ID
            body += " "
            body += str(entry.time.year) + "%02d" % int(entry.time.month) + "%02d" % int(entry.time.day)
            body += "%02d" % int(entry.time.hour) + "%02d" % int(entry.time.minute)
            body += " "
            body += "%.2f" % tempc
            body += " "
            body += "%.2f" % entry.humidity
            body += " "
            body += "%.2f" % entry.wind_speed
            body += " "
            body += entry.wind_direction
            body += " "
            body += "%.2f" % entry.wind_gust
            body += " X X "
            body += "%.2f" % entry.rainfall
            body += " "
            body += "%.2f" % entry.rainfall_rate
            body += " X\n"
        return body

class WSInput(webapp2.RequestHandler):
    # TODO: DOS protection by blacklisting incorrectly programmed keys?
    def post(self):
        # Input from Arduino
        ip = self.request.remote_addr
        try:
            # Grab data from body/headers
            authentication = self.request.headers['key']
            if (authentication != keys.WS_KEY):
                raise Exception('API Key incorrect (Tried submitting to WSInput).')
            # Data types {time: datetime, wind_speed: float, wind_direction: string, wind_gust: float, rainfall: float}
            #            {humidity: float, temperature: float, pressure: float}
            time           = datetime.utcfromtimestamp(float(self.request.POST.get('time')))
            # Make sure this isn't messing up timezones with weather station (everything should be UTC)
            wind_speed     = float(self.request.POST.get('wind_speed'))
            wind_direction = str(self.request.POST.get('wind_direction'))
            wind_gust      = float(self.request.POST.get('wind_gust'))
            rainfall       = float(self.request.POST.get('rainfall'))
            rainfall_rate  = float(self.request.POST.get('rainfall_rate'))
            humidity       = float(self.request.POST.get('humidity'))
            temperature    = float(self.request.POST.get('temperature'))
            pressure       = float(self.request.POST.get('pressure'))
            WeatherStation.Insert(time,
                                  wind_speed,
                                  wind_direction,
                                  wind_gust,
                                  rainfall,
                                  rainfall_rate,
                                  humidity,
                                  temperature,
                                  pressure)
            self.response.out.write("Success.")
        except Exception as err:
            # Something went wrong, notify user and TODO: Log IP
            # If three (3) bad requests are made, blacklist
            if not err:
                err = "Something went wrong while making a request to WSInput"
            # TODO: Update tries remaining by checking with log
            tries_remaining = 1
            self.response.out.write(repr(err) + "\n" + str(tries_remaining) + " tries remaining.")
            # EmailRequest.unauthorizedAccess(ip)


# API Request from browser
class UpdateData(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        param = []
        param.append(Cities.GetValues("Sacramento"))
        param.append(Cities.GetValues("Washington"))
        param.append(Cities.GetValues("Tampa"))
        # ws = WeatherStation.GetValues()
        encoding = Formatter.formatWU(param, [])
        self.response.out.write(encoding)


# When client tells us stuff is wrong
class ErrorInput(webapp2.RequestHandler):
    def post(self):
        message = self.request.POST.get('message')
        EmailRequest.serviceRequest(message)
        self.response.out.write("Message received by server.")


class SubmitGLOBE(webapp2.RequestHandler):
    def get(self):
        vals = WeatherStation.GetValues()
        vals = Formatter.formatWS(vals)
        EmailRequest.sendGLOBE(vals)


class VerifyWeatherUnderground(webapp2.RequestHandler):
    def get(self):
        WeatherUnderground.verifyData()


class UpdateWeatherUnderground(webapp2.RequestHandler):
    def get(self):
        WeatherUnderground.updateData()

#########################################################
###                                                   ###
###                Weather Underground                ###
###                                                   ###
#########################################################

class WeatherUnderground:
    citydict = {"Sacramento": "CA", "Tampa": "FL", "Washington": "DC"}
    cities = ["Sacramento", "Tampa", "Washington"]
    minuteCalls = 0
    dailyCalls = 0
    timeSinceLastCall = datetime.now()

    # Call in the case that the history of a location needs to be found
    @classmethod
    def callWUHistory(cls, d, location):
        """
        Calls Weather Underground API with given key (found in API_Keys.py).
        Parameters:
            d: Date in form YYYYMMDD
            location: one of the cities
        Returns:
            Parsed json format
        """
        if WeatherUnderground.canMakeCall():
            url = "https://api.wunderground.com/api/" + keys.WU + "/history_" + d + "/q/" + cls.citydict[location] + "/" + location + ".json"
            request = urllib2.Request(url)
            try:
                response = urllib2.urlopen(request)
                json_string = response.read()
                parsed_json = json.loads(json_string)
                response.close()
                print "Request date: " + parsed_json["history"]["date"]["pretty"]
                return parsed_json
            except:
                return None
        else:
            return None

    # Normal call every 15 minutes for current conditions
    @classmethod
    def callWUConditions(cls, location):
        """
        Calls Weather Underground API with given key (found in API_Keys.py).
        Returns:
            Parsed json format
        """
        if WeatherUnderground.canMakeCall():
            url = "https://api.wunderground.com/api/" + keys.WU + "/conditions/q/" + cls.citydict[location] + "/" + location + ".json"
            request = urllib2.Request(url)
            try:
                response = urllib2.urlopen(request)
                json_string = response.read()
                parsed_json = json.loads(json_string)
                response.close()
                return parsed_json
            except:
                return None
        else:
            return None

    @classmethod
    def canMakeCall(cls):
        # Assume daily call limits reset at midnight EST
        now = datetime.now()
        # Gives two hour window
        diffBetweenMidnight = int((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).seconds)
        diffBetweenTimes = int((now - cls.timeSinceLastCall).seconds)
        print "Times: " + str(diffBetweenTimes)
        if diffBetweenMidnight > diffBetweenTimes:
            cls.dailyCalls = 0
        if (now - cls.timeSinceLastCall).seconds > 59:
            cls.timeSinceLastCall = now
            cls.minuteCalls = 0

        if cls.minuteCalls < 9 and cls.dailyCalls < 450:
            cls.minuteCalls += 1
            cls.dailyCalls += 1
            cls.timeSinceLastCall = now
            return True
        else:
            return False

    # Check if all data is there (NDB request first), if not call then correct data
    @classmethod
    def verifyData(cls):
        # Check if there are any missing values every hour
        now = datetime.now()
        for city in cls.cities:
            db = Cities.GetValues(city)

            # Check for values older than 30 days, if any exist then delete them
            # Also remove duplicate values
            for entry in range(len(db)):
                diff = db[entry].time - now
                if (diff.days > 30 or db[entry].time == db[(entry + 1) % len(db)].time):
                    db[entry].key.delete()
                else:
                    # Since fetch is ordered by time, break out of loop as soon as days <= 30
                    break

            # Find date of missing values
            if len(db) > 0:
                # Database already exists, time is the first entity in array
                latestHour = db[0].time
            else:
                # Start off DB
                date = datetime.now() + td.timedelta(-29)
                latestHour = date
                hour = "%02d" % now.hour
                date = str(date.year) + "%02d" % date.month + "%02d" % date.day
                WeatherUnderground.findData(date, city, hour)
                date = now + td.timedelta(-28)
                hour = "%02d" % date.hour
                date = str(date.year) + "%02d" % date.month + "%02d" % date.day
                WeatherUnderground.findData(date, city, hour)

            for entry in db:
                # Check to see if the time difference is over an hour, ignore it if it's within 24 hours
                ### Issues with initial loading of db - not sure if regular running is fine ###
                if int((now - entry.time).days) < 2:
                    continue
                diff = True and int((entry.time - latestHour).seconds / 3600) or int((entry.time - latestHour).days) * 24
                print "Diff: " + str(diff)
                if diff > 1:
                    # print "MISSING"
                    # We're missing at least one hour
                    for hr in range(1, diff + 1):
                        entrytime = entry.time + td.timedelta(seconds = hr * 3600 * -1)
                        date = str(entrytime.year) + "%02d" % entrytime.month + "%02d" % entrytime.day
                        city = entry.city
                        hour = "%02d" % entrytime.hour
                        WeatherUnderground.findData(date, city, hour)
                else:
                    latestHour = entry.time
            # print "CITY END"

    @staticmethod
    def findData(date, city, hour):
        # Attempt to find data from Weather Underground's history
        history = WeatherUnderground.callWUHistory(date, city)
        if history is None:
            # print "History is none (Max calls reached)"
            return
        history = history["history"]["observations"]
        foundTime = False
        while not foundTime:
            for conditions in history:
                if (conditions["utcdate"]["hour"] == hour):
                    foundTime = True
                    overview = conditions["utcdate"]
                    time = datetime(int(overview["year"]), int(overview["mon"]), int(overview["mday"]), int(overview["hour"]), int(overview["min"]))
                    try:
                        wind_speed = float(conditions["wspdi"])
                    except:
                        wind_speed = None
                    try:
                        wind_direction = str(conditions["wdire"])
                    except:
                        wind_direction = None
                    try:
                        wind_gust = float(conditions["wgusti"]) if float(conditions["wgusti"]) > 0.00 else 0.00
                    except:
                        wind_gust = 0.00
                    try:
                        rainfall = float(conditions["precipi"]) if float(conditions["precipi"]) > 0.00 else 0.00
                    except:
                        rainfall = 0.00
                    try:
                        humidity = conditions["hum"]
                        humidity = humidity.strip("%\n ")
                        humidity = float(humidity)
                    except:
                        humidity = None
                    try:
                        temperature = float(conditions["tempi"])
                    except:
                        temperature = None
                    try:
                        pressure = float(conditions["pressurei"])
                    except:
                        pressure = None
                    # Data types {city: String, time: datetime, wind_speed: float, wind_direction: string, wind_gust: float}
                    #            {rainfall: float, humidity: float, temperature: float, pressure: float}
                    Cities.Insert(city, time, wind_speed, wind_direction, wind_gust, rainfall, humidity, temperature, pressure)
                    break # Exit for loop after finding the right hour
            # Try to find an hour close to x days ago if one isn't present
            # Done with strings so can't get conversion errors if JSON return None or like value
            hour = "%02d" % ((int(hour) - 1) % 24)

    # Update current conditions, delete any data older than 30 days
    @classmethod
    def updateData(cls):
        # return 1 # REMOVE WHEN READY
        # Traverse through all three ciites
        for city in cls.cities:
            conditions = WeatherUnderground.callWUConditions(city)
            conditions = conditions["current_observation"]
            try:
                # Need to convert to UTC and timedate
                time = conditions["observation_epoch"] # Why is this in EST?, still need to convert to datetime
                time = datetime.utcfromtimestamp(int(time))
            except:
                continue
            try:
                wind_speed = float(conditions["wind_mph"])
            except:
                wind_speed = None
            try:
                wind_direction = str(conditions["wind_dir"])
            except:
                wind_direction = None
            try:
                wind_gust = float(conditions["wind_gust_mph"]) if float(conditions["wind_gust_mph"]) > 0.00 else 0.00
            except:
                wind_gust = 0.00
            try:
                rainfall = float(conditions["precip_today_in"]) if float(conditions["precip_today_in"]) > 0.00 else 0.00
            except:
                rainfall = 0.00
            try:
                humidity = conditions["relative_humidity"]
                humidity = humidity.strip("%\n ")
                humidity = float(humidity)
            except:
                humidity = None
            try:
                temperature = float(conditions["temp_f"])
            except:
                temperature = None
            try:
                pressure = float(conditions["pressure_in"])
            except:
                pressure = None
            # Data types {city: String, time: datetime, wind_speed: float, wind_direction: string, wind_gust: float}
            #            {rainfall: float, humidity: float, temperature: float, pressure: float}
            Cities.Insert(city, time, wind_speed, wind_direction, wind_gust, rainfall, humidity, temperature, pressure)
        # Cleanup
        # TODO: Fix once db conditions are functioning normally
        # Cities.RemoveOldestValue()
