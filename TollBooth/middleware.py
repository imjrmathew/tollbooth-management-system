import datetime
from datetime import timedelta
from django.utils.deprecation import MiddlewareMixin

from CustomerDashboard.models import Booking


class ReferMiddleware(MiddlewareMixin):
    def process_request(self, request):
        bobj = Booking.objects.filter(isCanceled=False, isExpired=False)
        todaydate = datetime.datetime.now()
        for i in bobj:
            tempdate = i.DateExpired
            temptime = i.TimeExpired
            finaldatetime = str(tempdate)+" "+str(temptime)
            databasedatetime = datetime.datetime.strptime(finaldatetime, '%Y-%m-%d %H:%M:%S.%f')
            if databasedatetime < todaydate:
                i.isExpired = True
                i.save()
