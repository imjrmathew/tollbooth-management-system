from builtins import getattr
from datetime import timedelta
import datetime
import json
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from .models import *
from Home.models import *
from AdminDashboard.models import *
# Create your views here.


def CustomerIndex(request):
    logid = request.session['userid']
    datime = datetime.date.today()
    noofbooths = AddToll.objects.filter(isdeleted=False).count()
    noofveh = VehicleReg.objects.filter(isdeleted=False, loginid=request.session['userid']).count()
    bookobj = Booking.objects.filter(loginid=logid, isCanceled=False, VehicleID__isdeleted=False).order_by('-id')
    noofbooking = Booking.objects.filter(loginid=logid, isExpired=False, isCanceled=False).count()
    context = {
        'datetime': datime,
        'noofbooths': noofbooths,
        'noofveh': noofveh,
        'bookobj': bookobj,
        'noofbooking': noofbooking,
    }
    return render(request, "CustomerDashboard/customerIndex.html", context)


def AddVehicleReg(request):
    id = request.session['userid']
    category = AddVehicle.objects.filter(isdeleted=False)
    if request.method == "POST":
        vtype = request.POST.get('category')
        regno = request.POST.get('regnum')

        vreg = VehicleReg()
        lobj = Login.objects.get(pk=id)
        print(lobj)
        vobj = AddVehicle.objects.get(VehicleType=vtype, isdeleted=False)
        vreg.loginid = lobj
        vreg.VehicleTypeID = vobj
        vreg.VehicleRegNum = regno
        vreg.isdeleted = False
        if VehicleReg.objects.filter(VehicleRegNum=regno).filter(isdeleted=False).exists():
            messages.warning(request, "Already Exist!")
            return HttpResponseRedirect('/Customers/ListVehicleReg')
        else:
            vreg.save()
            messages.success(request, "Added Successfully")
            return HttpResponseRedirect('/Customers/ListVehicleReg')
    return render(request, "CustomerDashboard/customerListVehicle.html", {'category': category})


def EditVehicleReg(request, pk):
    vob = VehicleReg.objects.get(pk=pk)
    data = {
        'Id': vob.pk,
        'VehicleType': vob.VehicleTypeID.VehicleType,
        'VehicleReg': vob.VehicleRegNum
    }
    return JsonResponse(data)


def UpdateVehicleReg(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('id')
        vtype = request.POST.get('VehicleType')
        vreg = request.POST.get('VehicleReg')
        vobj = AddVehicle.objects.get(VehicleType=vtype, isdeleted=False)
        vehobj = VehicleReg.objects.get(pk=id)
        vehobj.VehicleTypeID = vobj
        vehobj.VehicleRegNum = vreg
        if VehicleReg.objects.filter(VehicleRegNum=vreg).filter(isdeleted=False).exists():
            message = {'error': "Already exists"}
            messages.warning(request, "Already Exist!")
            return JsonResponse(message)
        else:
            vehobj.save()
            message = {'message': 'Success'}
            messages.success(request, "Updated Successfully")
            return JsonResponse(message)


def DeleteVehicleReg(request, pk):
    vob = VehicleReg.objects.get(pk=pk)
    vob.isdeleted = True
    if Booking.objects.filter(VehicleID=pk, isCanceled=False).exists():
        bob = Booking.objects.get(VehicleID=pk, isCanceled=False)
        bob.isCanceled = True
        bob.isExpired = True
        bob.save()
    vob.save()
    messages.error(request, "Deleted Successfully")
    return HttpResponseRedirect('/Customers/ListVehicleReg')


def ListVehicleReg(request):
    id = request.session['userid']
    details = Registration.objects.get(loginid=id)
    vehdetails = VehicleReg.objects.filter(isdeleted=False, loginid=id)
    category = AddVehicle.objects.filter(isdeleted=False).order_by('-VehicleType')
    context = {
        'vehdetails': vehdetails,
        'category': category,
        'details': details,
    }
    return render(request, "CustomerDashboard/customerListVehicle.html", context)


def BookNow(request):
    id = request.session['userid']
    details = Registration.objects.get(loginid=id)
    regdetails = VehicleReg.objects.filter(loginid=id, isdeleted=False)
    vehdetails = AddVehicle.objects.filter(isdeleted=False)
    location = AddToll.objects.filter(isdeleted=False)
    toll = AddToll.objects.filter(isdeleted=False)
    context = {
        'details': details,
        'vehdetails': vehdetails,
        'regdetails': regdetails,
        'location': location,
        'toll': toll,
    }
    if request.method == "POST":
        logid = request.session['userid']
        vreg = request.POST.get('meid')
        vtype = request.POST.get('mevtid')
        tollid = request.POST.get('mtid')
        dtbook = request.POST.get('datebooked')
        dtexpired = request.POST.get('menowexdate')
        log = Login.objects.get(pk=logid)
        tempmail = Registration.objects.get(loginid=logid)
        toll = AddToll.objects.get(pk=tollid)
        vregistration = VehicleReg.objects.get(pk=vreg)
        tempamnt = AddPriceCharge.objects.filter(TollID=tollid, VehicleTypeID=vtype).values_list('pk', flat=True)
        amountobj = AddPriceCharge.objects.get(pk=tempamnt[0])

        bookobj = Booking()
        try:
            orderpk = Booking.objects.latest('pk')
            orderid = int(orderpk.pk) + 1
        except:
            orderid = 1
        bookobj.loginid = log
        bookobj.TollID = toll
        bookobj.DateBooked = dtbook
        bookobj.TimeBooked = datetime.datetime.now().time()
        bookobj.TimeExpired = datetime.datetime.now().time()
        bookobj.DateExpired = dtexpired
        bookobj.VehicleID = vregistration
        bookobj.AmountID = amountobj
        if Booking.objects.filter(VehicleID=vreg, TollID=tollid, DateBooked=dtbook, isExpired=False,
                                  isCanceled=False).exists():
            messages.warning(request, "Already Exist!")
            return HttpResponseRedirect('/Customers/Booking')
        else:
            return render(request, "CustomerDashboard/Checkout.html", {'content': bookobj, 'temp': tempmail, 'orderid': orderid})
    return render(request, "CustomerDashboard/customerBooking.html", context)


def Checkout(request):
    loginid = request.POST.get('loginid')
    tollid = request.POST.get('tollid')
    datebooked = request.POST.get('datebooked')
    dateexpired = request.POST.get('dateexpired')
    vehicleid = request.POST.get('vehicleid')
    amountid = request.POST.get('amountid')

    log = Login.objects.get(pk=loginid)
    toll = AddToll.objects.get(pk=tollid)
    vregistration = VehicleReg.objects.get(pk=vehicleid)
    amountobj = AddPriceCharge.objects.get(pk=amountid)
    email = Registration.objects.get(loginid=loginid)

    bookobj = Booking()
    bookobj.loginid = log
    bookobj.TollID = toll
    bookobj.DateBooked = datebooked
    bookobj.TimeBooked = datetime.datetime.now().time()
    bookobj.TimeExpired = datetime.datetime.now().time()
    bookobj.DateExpired = dateexpired
    bookobj.VehicleID = vregistration
    bookobj.AmountID = amountobj
    bookobj.isExpired = False
    bookobj.isCanceled = False
    bookobj.save()
    context = {
        'bookobj': bookobj
    }
    subject, from_email, to = 'Order Details of BookingID# {}'.format(bookobj.pk), 'YOUR MAIL ID', str(email.Email)
    text_content = 'Hi,' + bookobj.loginid.username + ', \nYour order for BookingID# '+ str(bookobj.pk) +' was succesfully booked on '+ str(bookobj.DateBooked) +' for the TollBooth '+ bookobj.TollID.TollName+ '.\nRegard dN'
    html_content = render_to_string('CustomerDashboard/bookingmail.html', context)
    mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
    mail.attach_alternative(html_content, "text/html")
    mail.send()
    messages.success(request, "Hello {0}, Your BookingID# {1} has booked succesfully ".format(log.username, bookobj.pk))
    return HttpResponseRedirect('/Customers/ListBooking')


def EditBooking(request, pk):
    lob = Booking.objects.get(pk=pk)
    vehid_object = Booking._meta.get_field('VehicleID')
    vehid = vehid_object.value_from_object(lob)

    vtypeob = VehicleReg.objects.get(pk=vehid)
    vtype_object = VehicleReg._meta.get_field('VehicleTypeID')
    vtypeid = vtype_object.value_from_object(vtypeob)

    tollid_object = Booking._meta.get_field('TollID')
    tollid = tollid_object.value_from_object(lob)

    routeob = AddToll.objects.get(pk=tollid)
    route_object = AddToll._meta.get_field('RouteID')
    routeid = route_object.value_from_object(routeob)

    data = {
        'ID': lob.pk,
        'rno': lob.VehicleID.VehicleRegNum,
        'rnoid': vehid,
        'vtype': lob.VehicleID.VehicleTypeID.VehicleType,
        'vtypeid': vtypeid,
        'tbooth': lob.TollID.TollName,
        'tboothid': tollid,
        'routeid': routeid,
        'sloc': lob.TollID.RouteID.SourceLoc.CityName,
        'dloc': lob.TollID.RouteID.DestinationLoc.CityName,
        'amount': lob.AmountID.Amount,
        'datebooked': lob.DateBooked,
        'dateexpired': lob.DateExpired,
    }
    return JsonResponse(data)


def UpdateBooking(request):
    if request.method == "POST":
        id = request.POST.get('mebookid')
        vreg = request.POST.get('meid')
        vtype = request.POST.get('mevtid')
        tollid = request.POST.get('mtid')
        dtbook = request.POST.get('datebooked')
        dtexpired = request.POST.get('menowexdate')

        toll = AddToll.objects.get(pk=tollid)
        vregistration = VehicleReg.objects.get(pk=vreg)
        tempamnt = AddPriceCharge.objects.filter(TollID=tollid, VehicleTypeID=vtype).values_list('pk', flat=True)
        amountobj = AddPriceCharge.objects.get(pk=tempamnt[0])

        bookobj = Booking.objects.get(pk=id)

        bookobj.TollID = toll
        bookobj.DateBooked = dtbook
        bookobj.TimeBooked = datetime.datetime.now().time()
        bookobj.TimeExpired = datetime.datetime.now().time()
        bookobj.DateExpired = dtexpired
        bookobj.VehicleID = vregistration
        bookobj.AmountID = amountobj
        bookobj.isExpired = False
        bookobj.isCanceled = False
        if Booking.objects.filter(VehicleID=vreg, TollID=tollid, DateBooked=dtbook, isExpired=False,
                                  isCanceled=False).exists():
            messages.warning(request, "Already Exist!")
            return HttpResponseRedirect('/Customers/ListBooking')
        else:
            bookobj.save()
            messages.success(request, "Updated Successfully")
            return HttpResponseRedirect('/Customers/ListBooking')


def CancelBooking(request):
    logid = request.session['userid']
    bookobj = Booking.objects.filter(loginid=logid, isCanceled=False, VehicleID__isdeleted=False).order_by('-id')
    context = {
        'bookobj': bookobj,
    }
    if request.method == "POST":
        id = request.POST.get('deleteidme')
        bookobject = Booking.objects.get(pk=id)
        bookobject.isCanceled = True
        bookobject.isExpired = True
        bookobject.save()
        messages.error(request, "Canceled Successfully, Your payment will be refunded shortly.")
        return HttpResponseRedirect('/Customers/ListBooking')
    return render(request, "CustomerDashboard/customerListBooking.html", context)


def ListBooking(request):
    logid = request.session['userid']
    details = Registration.objects.get(loginid=logid)
    regdetails = VehicleReg.objects.filter(loginid=logid, isdeleted=False)
    vehdetails = AddVehicle.objects.filter(isdeleted=False)
    location = AddToll.objects.filter(isdeleted=False)
    toll = AddToll.objects.filter(isdeleted=False)
    bookobj = Booking.objects.filter(loginid=logid, isCanceled=False, VehicleID__isdeleted=False).order_by('-id')
    context = {
        'bookobj': bookobj,
        'details': details,
        'vehdetails': vehdetails,
        'regdetails': regdetails,
        'location': location,
        'toll': toll,
    }
    return render(request, "CustomerDashboard/customerListBooking.html", context)


def GetRegValue(request, pk):
    vob = VehicleReg.objects.get(pk=pk)
    field_object = VehicleReg._meta.get_field('VehicleTypeID')
    field_value = field_object.value_from_object(vob)
    vehid = field_value
    data = {
        'Id': vob.pk,
        'tid': vehid,
        'VehicleType': vob.VehicleTypeID.VehicleType,
    }
    return JsonResponse(data)


def GetTollValue(request, pk):
    temp = json.loads(pk)
    pks = temp[0]
    ids = temp[1]
    tob = AddToll.objects.get(pk=pks)
    field_object = AddToll._meta.get_field('RouteID')
    field_value = field_object.value_from_object(tob)
    routeid = field_value
    amobj = AddPriceCharge.objects.filter(TollID=pks, VehicleTypeID=ids).values_list('Amount', flat=True)
    if amobj:
        amount = amobj[0]
    else:
        amount = "0.00"
    rob = AddRoute.objects.get(pk=routeid)
    data = {
        'Id': tob.pk,
        'routeid': routeid,
        'SourceLoc': rob.SourceLoc.CityName,
        'DestinationLoc': rob.DestinationLoc.CityName,
        'Amount': amount,
    }
    return JsonResponse(data)


def GetExpiry(request, pk):
    dat = json.loads(pk)
    time = datetime.datetime.now().time()
    dattime = str(dat)+" "+str(time)
    conversion = datetime.datetime.strptime(dattime, '%Y-%m-%d %H:%M:%S.%f')
    expiry = conversion + timedelta(days=1)
    converteddate = conversion.date()
    expirydate = expiry.date()
    data = {
        'currentdate': converteddate,
        'expirydate': expirydate,
    }
    return JsonResponse(data)


def UpdateProfile(request):
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
            return HttpResponseRedirect('/Customers/UpdateProfile')
        else:
            return render(request, "CustomerDashboard/customerProfile.html", {'number': 'Invalid Number'})
    return render(request, "CustomerDashboard/customerProfile.html")



def UpdatePassword(request):
    id = request.session['userid']
    if request.method == "POST":
        password = request.POST.get('newpassword')
        logobj = Login.objects.get(pk=id)
        logobj.password = make_password(password, salt=None, hasher='default')
        logobj.save()
        messages.success(request, "Password Changed Successfully")
        return HttpResponseRedirect('/Customers/UpdateProfile')
    return render(request, "CustomerDashboard/customerProfile.html")


def DeleteAccount(request):
    id = request.session['userid']
    logobj = Login.objects.get(pk=id)
    logobj.isdeleted = True
    logobj.save()
    return HttpResponseRedirect('/logout')

