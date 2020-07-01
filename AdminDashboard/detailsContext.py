from Home.models import *
from CustomerDashboard.models import Booking


def DetailsContext(request):
    id = request.session.get('userid',None)
    try:
        logindetails = Login.objects.get(pk=id)
        userdetails = Registration.objects.get(loginid=id)
        bookobjs = Booking.objects.filter().order_by('-id')
        newuserobjs = Registration.objects.filter()
    except:
        logindetails = None
        userdetails = None
        bookobjs = None
        newuserobjs = None
    return {
        'logindetails': logindetails,
        'userdetails': userdetails,
        'bookobjs': bookobjs,
        'newuserobjs': newuserobjs,
    }