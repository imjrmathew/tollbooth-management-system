import datetime
from Home.models import *


def DetailsContext(request):
    date = datetime.date.today()
    id = request.session.get('userid', None)
    try:
        logindetails = Login.objects.get(pk=id)
        userdetails = Registration.objects.get(pk=id)
    except:
        logindetails = None
        userdetails = None
    return {
        'logindetails': logindetails,
        'userdetails': userdetails,
        'dates': str(date),
    }
