from django.contrib.auth.models import User
from CustomerDashboard.models import *
from Home.models import *


def DetailsContext(request):
    id = request.session.get('userid',None)
    try:
        tollob = TollRegisterAdditional.objects.get(workerid__loginid=id)
        field_object = TollRegisterAdditional._meta.get_field('Tollid')
        field_value = field_object.value_from_object(tollob)
        bookobj = Booking.objects.filter(TollID=field_value, VehicleID__isdeleted=False).order_by('-id')
        newuserobj = Registration.objects.filter()
        logindetails = Login.objects.get(pk=id)
        userdetails = Registration.objects.get(loginid=id)
    except:
        logindetails = None
        userdetails = None
        bookobj = None
        newuserobj = None
    return {
        'logindetails': logindetails,
        'userdetails': userdetails,
        'bookobj': bookobj,
        'newuserobj': newuserobj
    }