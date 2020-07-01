import base64
import datetime
import json
import io
import os
from google.cloud import vision_v1p3beta1 as vision
import cv2
import pandas as pd
from PIL import Image
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from CustomerDashboard.models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from AdminDashboard.models import *
from Home.models import *
from TollBooth import settings

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(settings.CHECK_IMG, 'JSON FILE NAME')
SOURCE_PATH = settings.CHECK_IMG


# Create your views here.


def index(request):
    id = request.session['userid']
    datime = datetime.date.today()
    route = Registration.objects.get(loginid=id, loginid__isdeleted=False, loginid__roleid=2)
    routeid = TollRegisterAdditional.objects.get(workerid=route.id)
    routename = routeid.Tollid.TollName
    routenam = routename.replace('TBooth', "")
    noofworkersrt = TollRegisterAdditional.objects.filter(workerid__loginid__roleid=2,
                                                          workerid__loginid__isdeleted=False,
                                                          Tollid__TollName=routename).count()
    noofworkers = Login.objects.filter(roleid=2, isdeleted=False, isapproved=True, status=True).count()
    noofbooths = AddToll.objects.filter(isdeleted=False).count()
    tollob = TollRegisterAdditional.objects.get(workerid__loginid=id)
    field_object = TollRegisterAdditional._meta.get_field('Tollid')
    field_value = field_object.value_from_object(tollob)
    noofbooking = Booking.objects.filter(isCanceled=False, TollID=field_value, isExpired=False).count()
    context = {
        'datetime': datime,
        'noofworkers': noofworkers,
        'noofbooths': noofbooths,
        'routename': routenam,
        'noofworkersrt': noofworkersrt,
        'noofbooking': noofbooking
    }
    return render(request, "WorkersDashboard/workersIndex.html", context)


def WorkersLists(request):
    workerid = request.session["tollid"]
    tollobj = TollRegisterAdditional.objects.get(workerid=workerid)
    field_object = TollRegisterAdditional._meta.get_field('Tollid')
    field_value = field_object.value_from_object(tollobj)
    log = TollRegisterAdditional.objects.select_related().filter(Tollid=field_value, workerid__loginid__isapproved=True,
                                                                 workerid__loginid__status=True,
                                                                 workerid__loginid__isdeleted=False,
                                                                 workerid__loginid__roleid=2)
    return render(request, "WorkersDashboard/workersWorkersList.html", {'log': log})


def ListRoutes(request):
    location = AddLocations.objects.filter(isdeleted=False)
    routeob = AddRoute.objects.select_related().filter(isdeleted=False)
    return render(request, "WorkersDashboard/workersListRoute.html", {'routeobj': routeob, 'location': location})


def ListTollBooths(request):
    routes = AddRoute.objects.filter(isdeleted=False)
    tolls = AddToll.objects.select_related().filter(isdeleted=False)
    return render(request, "WorkersDashboard/workersListTollBooth.html", {'routes': routes, 'tolls': tolls})


def ListAmounts(request):
    workerid = request.session["tollid"]
    tollobj = TollRegisterAdditional.objects.get(workerid=workerid)
    field_object = TollRegisterAdditional._meta.get_field('Tollid')
    field_value = field_object.value_from_object(tollobj)
    stoll = AddToll.objects.filter(isdeleted=False)
    vtype = AddVehicle.objects.filter(isdeleted=False)
    charge = AddPriceCharge.objects.select_related().filter(isdeleted=False, TollID=field_value)
    return render(request, "WorkersDashboard/workersAmount.html", {'vtype': vtype, 'charge': charge, 'stoll': stoll})


def EditProfile(request):
    toll = AddToll.objects.filter(isdeleted=False)
    return render(request, "WorkersDashboard/workersProfile.html", {'tolls': toll})


def UpdateProfile(request):
    toll = AddToll.objects.filter(isdeleted=False)
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone = request.POST.get('mobile')

        id = request.session['userid']
        logobj = Login.objects.get(pk=id)
        logobj.username = username
        logobj.save()
        regobj = Registration.objects.get(loginid=id)
        regobj.FirstName = firstname
        regobj.LastName = lastname
        regobj.Address = address
        regobj.Email = email
        regobj.Phone = phone
        if phone.isdigit() and len(phone) == 10 or len(phone) == 12:
            regobj.save()
            messages.success(request, "Updated Successfully")
            return HttpResponseRedirect('/Workers/EditProfile')
        else:
            toll = AddToll.objects.filter(isdeleted=False)
            return render(request, "WorkersDashboard/workersProfile.html", {'tolls': toll, 'number': 'Invalid Number'})
    return render(request, "WorkersDashboard/workersProfile.html", {'tolls': toll})


def UpdatePassword(request):
    id = request.session['userid']
    if request.method == "POST":
        password = request.POST.get('newpassword')
        logobj = Login.objects.get(pk=id)
        logobj.password = make_password(password, salt=None, hasher='default')
        logobj.save()
        messages.success(request, "Password Changed Successfully")
        return HttpResponseRedirect('/Workers/EditProfile')
    return render(request, "WorkersDashboard/workersProfile.html")


def DeleteAccount(request):
    id = request.session['userid']
    logobj = Login.objects.get(pk=id)
    logobj.isdeleted = True
    logobj.save()
    return HttpResponseRedirect('/logout')


def BookingHistory(request):
    return render(request, "WorkersDashboard/workersBooking.html")


def CheckStatus(request):
    loginid = request.session['userid']
    dates = datetime.datetime.now().date()
    tollob = TollRegisterAdditional.objects.get(workerid__loginid=loginid)
    bookob = Booking.objects.filter(TollID=tollob.Tollid, isCanceled=False, isExpired=False,
                                    DateBooked=dates).order_by('-pk') | Booking.objects.filter(TollID=tollob.Tollid, isCanceled=False,
                                                                               isExpired=False, DateExpired=dates).order_by('-pk')
    context = {
        'booking': bookob
    }
    return render(request, "WorkersDashboard/workersCheck.html", context)


@csrf_exempt
def SaveImage(request):
    getfinalnumber = ""
    loginid = request.session['userid']
    if request.method == "POST":
        dir = settings.CHECK_IMG
        counter = 1
        payload = json.loads(request.body)
        image_data = payload['imageData']
        format, imgstr = image_data.split(';base64,')
        data = ContentFile(base64.b64decode(imgstr))
        imageobj = Image.open(data)
        rotatatedimg = imageobj.transpose(Image.FLIP_LEFT_RIGHT)
        finaldir = ""
        myfile = ""
        while counter > 0:
            myfile = "image-" + str(counter) + ".png"
            finaldir = os.path.join(dir, myfile)
            if os.path.isfile(finaldir):
                counter += 1
            else:
                break
        imageobj.save(finaldir)
        getfinalnumber = SearchNumber(myfile, loginid)
        data = {'msg': str(getfinalnumber)}
        return JsonResponse(data)


def SearchNumber(myfile, loginid):
    finalnumber = ""
    img_path = os.path.join(settings.CHECK_IMG, myfile)
    dates = datetime.datetime.now().date()
    tollob = TollRegisterAdditional.objects.get(workerid__loginid=loginid)
    bookobs = Booking.objects.filter(TollID=tollob.Tollid, isCanceled=False, isExpired=False,
                                     DateBooked=dates) | Booking.objects.filter(TollID=tollob.Tollid, isCanceled=False,
                                                                                isExpired=False, DateExpired=dates)
    trial = []
    for i in bookobs:
        getst = str(i.VehicleID.VehicleRegNum)
        trial.append(getst)
    number = []
    for i in bookobs:
        getstring = str(i.VehicleID.VehicleRegNum).replace('-', "")
        number.append(getstring)

    img = cv2.imread(img_path)
    height, width = img.shape[:2]
    img = cv2.resize(img, (800, int((height * 800) / width)))
    imgs = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgb = cv2.bilateralFilter(imgs, 11, 17, 17)

    outputpath = os.path.join(settings.OUTPUTPATH, 'outputimage.png')
    cv2.imwrite(outputpath, imgb)
    img_path = outputpath

    client = vision.ImageAnnotatorClient()

    with io.open(img_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    df = pd.DataFrame(columns=['description'])
    for obj in texts:
        df = df.append(
            dict(
                description=obj.description,
            ),
            ignore_index=True
        )
    print(df)
    if df.empty:
        finalnumber = "The Number is not found!"
        return finalnumber
    temp = []
    val = ""
    for i in df.description:
        val = val + i
        temp.append(val)
    inpu = [''.join(x) for x in zip(*[iter(temp[-1])] * 1)]

    new = []
    for i in number:
        news = [''.join(x) for x in zip(*[iter(i)] * 1)]
        new.append(news)

    count = 0
    for k in new:
        count += 1

    checkvalue = [[] for _ in range(count)]
    for j in range(count):
       for i in new[j]:
           if i in inpu:
               checkvalue[j].append('1')
           else:
               checkvalue[j].append('0')

    for k in range(len(checkvalue)):
        counter = 0
        for z in checkvalue[k]:
            if '1' in z:
                counter += 1
        if counter == len(checkvalue[k]):
            finalnumber = trial[k]
            finalnumber = str(finalnumber) + " is registered."
        else:
            finalnumber = "The Number is not found!"
    return finalnumber
