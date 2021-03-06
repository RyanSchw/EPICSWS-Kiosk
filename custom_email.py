from google.appengine.api import mail
import API_Keys as keys
import webapp2
from datetime import datetime
import os

# Sender can be XXXX@kiosk-application.appspotmail.com or any verified person (selected in browser)


# Sends EPICS mentors an email telling them that the weather station needs servicing
class EmailRequest:
    timeSinceLastCall = datetime.now()
    dailyCalls = 0

    @classmethod
    def canMakeCall(cls):
        if int(float(os.environ['WEBSITE_VERSION'])) > 0:
            return False
        # TODO: Limit so that service requests are sent out once a day
        now = datetime.now()
        diffBetweenTimes = int((now - cls.timeSinceLastCall).days)
        if diffBetweenTimes > 0:
            cls.dailyCalls = 0
        elif diffBetweenTimes == 0:
            diffBetweenMidnight = int((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).seconds)
            diffBetweenTimes = int((now - cls.timeSinceLastCall).seconds)
            if diffBetweenMidnight > diffBetweenTimes:
                cls.dailyCalls = 0

        if cls.dailyCalls < 9:
            cls.dailyCalls += 1
            cls.timeSinceLastCall = now
            return True
        else:
            return False

    @staticmethod
    def serviceRequest(errorMsg):
        message = mail.EmailMessage(sender = keys.SERVICE_EMAIL,
                                    subject = "AUTOMATED EMAIL: Weather Station Service Request",
                                    body = "Attention: This is an automated email sent from kiosk-application.appspot.com. We have detected an error (listed below) that requires your attention.\n\n" + errorMsg)

        for recipient in keys.SITE_ADMINS:
            message.to = recipient
            if EmailRequest.canMakeCall():
                return
                # message.send()

    def unauthorizedAccess(ip):
        message = mail.EmailMessage(sender = keys.SERVICE_EMAIL,
                                    subject = "AUTOMATED EMAIL (ACTION REQUIRED): Weather Station Unauthorized Access",
                                    body = "Attention: This is an automated email sent from kiosk-application.appspot.com. We have detected an attempt to submit data to /request/submitws. More info is listed below\n\nIP:" + ip)

        for recipient in keys.SITE_ADMINS:
            message.to = recipient
            if EmailRequest.canMakeCall():
                return
                # message.send()
