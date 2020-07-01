import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

from AdminDashboard.models import *
from Home.models import *
from CustomerDashboard.models import *

# Create your views here.


def adminIndex(request):
    datime = datetime.date.today()
    noofusers = Login.objects.filter(roleid=3, isdeleted=False).count()
    noofworkers = Login.objects.filter(roleid=2, isdeleted=False, isapproved=True).count()
    noofbooths = AddToll.objects.filter(isdeleted=False).count()
    noofbooking = Booking.objects.filter(isCanceled=False, isExpired=False).count()
    context = {
        'datetime': datime,
        'noofusers': noofusers,
        'noofworkers': noofworkers,
        'noofbooths': noofbooths,
        'noofbooking': noofbooking,
    }
    return render(request, "AdminDashboard/adminindex.html", context)


def adminWorkersList(request):
    tolllog = TollRegisterAdditional.objects.filter(workerid__loginid__isdeleted=False, workerid__loginid__roleid=2).order_by('-pk')
    return render(request, "AdminDashboard/adminworkerslist.html", {'tolllog': tolllog})


def ApproveWorker(request, id):
    regobj = Registration.objects.get(pk=id)
    field_object = Registration._meta.get_field('loginid')
    field_value = field_object.value_from_object(regobj)
    log = Login.objects.get(pk=field_value)
    log.isapproved = True
    log.status = True
    log.save()
    messages.info(request, "Approved {}".format(log.username))
    return HttpResponseRedirect('/admindash/workerslist')


def RejectWorker(request, id):
    regobj = Registration.objects.get(pk=id)
    field_object = Registration._meta.get_field('loginid')
    field_value = field_object.value_from_object(regobj)
    log = Login.objects.get(pk=field_value)
    log.isapproved = False
    log.status = True
    log.save()
    messages.info(request, "Rejected {}".format(log.username))
    return HttpResponseRedirect('/admindash/workerslist')


def adminCustomerList(request):
    log = Registration.objects.select_related().filter(loginid__isdeleted=False).filter(loginid__roleid=3)
    vehdetails = VehicleReg.objects.filter(loginid__isdeleted=False, loginid__roleid=3, isdeleted=False)
    return render(request, "AdminDashboard/admincustomer.html", {'log':log, 'vehdetails': vehdetails})


def AddDistricts(request):
    if request.method == 'POST':
        districtname = request.POST.get('adddistrict')
        dist = AddDistrict()
        dist.DistrictName = districtname
        dist.isdeleted = False
        if AddDistrict.objects.filter(DistrictName=districtname).filter(isdeleted=False).exists():
            messages.warning(request, "Already Exist!")
            return HttpResponseRedirect('/admindash/ListDistrict')
        else:
            dist.save()
            messages.success(request, "Added Successfully")
            return HttpResponseRedirect('/admindash/ListDistrict')
    return render(request, "AdminDashboard/adminDistrictLocations.html")


def AddLocation(request):
    if request.method == 'POST':
        cityname = request.POST.get('addlocation')
        districtname = request.POST.get('district')
        did = AddDistrict.objects.get(DistrictName=districtname)
        loc = AddLocations()
        loc.CityName = cityname
        loc.DistrictId = did
        loc.isdeleted = False
        if AddLocations.objects.filter(CityName=cityname).filter(isdeleted=False).exists():
            messages.warning(request, "Already Exist!")
            return HttpResponseRedirect('/admindash/ListDistrict')
        else:
            loc.save()
            messages.success(request, "Added Successfully")
            return HttpResponseRedirect('/admindash/ListDistrict')
    return render(request, "AdminDashboard/adminDistrictLocations.html")


def EditDistrict(request, pk):
    dob = AddDistrict.objects.get(pk=pk)
    data = {
        'Id': dob.pk,
        'DistrictName': dob.DistrictName
    }
    return JsonResponse(data)


def UpdateDistrict(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('id')
        name = request.POST.get('DistrictName')
        dobj = AddDistrict.objects.get(pk=id)
        dobj.DistrictName = name
        if AddDistrict.objects.filter(DistrictName=name).filter(isdeleted=False).exists():
            message = {'error': "Already exists"}
            messages.warning(request, "Already Exist!")
            return JsonResponse(message)
        else:
            dobj.save()
            message = {'message': 'Success'}
            messages.success(request, "Updated Successfully")
            return JsonResponse(message)


def DeleteDistrict(request, pk):
    dob = AddDistrict.objects.get(pk=pk)
    dob.isdeleted = True
    if AddLocations.objects.filter(DistrictId=pk, isdeleted=False).exists():
        distdat = AddDistrict.objects.filter(isdeleted=False)
        locdat = AddLocations.objects.select_related().filter(isdeleted=False)
        context = {
            'nodelete': 'Can\'t Delete, Because {} is already in location'.format(dob.DistrictName),
            'distdat':distdat, 'locdata':locdat
        }
        return render(request, "AdminDashboard/adminDistrictLocations.html", context)
    else:
        dob.save()
        messages.error(request, "Deleted Successfully")
    return HttpResponseRedirect('/admindash/ListDistrict')


def EditLocation(request, pk):
    lob = AddLocations.objects.get(pk=pk)
    data = {
        'Id': lob.pk,
        'DistrictId': lob.DistrictId.DistrictName,
        'CityName': lob.CityName
    }
    return JsonResponse(data)


def UpdateLocation(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('id')
        dname = request.POST.get('DistrictId')
        lname = request.POST.get('CityName')
        dobj = AddDistrict.objects.get(DistrictName=dname)
        lobj = AddLocations.objects.get(pk=id)
        lobj.CityName = lname
        lobj.DistrictId = dobj
        if AddLocations.objects.filter(CityName=lname).filter(DistrictId=dobj.id).filter(isdeleted=False).exists():
            message = {'error': "Already exists"}
            messages.warning(request, "Already Exist!")
            return JsonResponse(message)
        else:
            lobj.save()
            message = {'message': 'Success'}
            messages.success(request, "Updated Successfully")
            return JsonResponse(message)


def DeleteLocation(request, pk):
    lob = AddLocations.objects.get(pk=pk)
    lob.isdeleted = True
    if AddRoute.objects.filter(SourceLoc=pk, isdeleted=False).exists() | AddRoute.objects.filter(DestinationLoc=pk, isdeleted=False).exists():
        distdat = AddDistrict.objects.filter(isdeleted=False)
        locdat = AddLocations.objects.select_related().filter(isdeleted=False)
        context = {
            'nolocation': 'Can\'t Delete, Because {} is already in route'.format(lob.CityName),
            'distdat':distdat, 'locdata':locdat
        }
        return render(request, "AdminDashboard/adminDistrictLocations.html", context)
    else:
        lob.save()
        messages.error(request, "Deleted Successfully")
        return HttpResponseRedirect('/admindash/ListDistrict')


def ListDistrictsLocation(request):
    distdat = AddDistrict.objects.filter(isdeleted=False)
    locdat = AddLocations.objects.select_related().filter(isdeleted=False)
    return render(request, "AdminDashboard/adminDistrictLocations.html", {'distdat':distdat, 'locdata':locdat})


def AddVehicleType(request):
    if request.method == "POST":
        vehtype = request.POST.get('vehtype')

        vehobj = AddVehicle()
        vehobj.VehicleType = vehtype
        vehobj.isdeleted = False
        if AddVehicle.objects.filter(VehicleType=vehtype, isdeleted=False).exists():
            messages.warning(request, "Already Exist!")
            return HttpResponseRedirect('/admindash/ListVehicleType')
        else:
            vehobj.save()
            messages.success(request, "Added Successfully")
            return HttpResponseRedirect('/admindash/ListVehicleType')
    return render(request, "AdminDashboard/adminAddVehType.html")


def EditVehicleType(request, pk):
    vob = AddVehicle.objects.get(pk=pk)
    data = {
        'Id': vob.pk,
        'VehicleType': vob.VehicleType,
    }
    return JsonResponse(data)


def UpdateVehicleType(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('id')
        vname = request.POST.get('VehicleType')
        vobj = AddVehicle.objects.get(pk=id)
        vobj.VehicleType = vname
        if AddVehicle.objects.filter(VehicleType=vname).filter(isdeleted=False).exists():
            message = {'error': "Already exists"}
            messages.warning(request, "Already Exist!")
            return JsonResponse(message)
        else:
            vobj.save()
            message = {'message': 'Success'}
            messages.success(request, "Updated Successfully")
            return JsonResponse(message)


def DeleteVehicleType(request, pk):
    vob = AddVehicle.objects.get(pk=pk)
    vob.isdeleted = True
    if AddPriceCharge.objects.filter(VehicleTypeID=pk, isdeleted=False).exists():
        vehicleobj = AddVehicle.objects.filter(isdeleted=False)
        context = {
            'novehicle': 'Can\'t Delete, Because there is an existing data for {}'.format(vob.VehicleType),
            'vehicleobj': vehicleobj
        }
        return render(request, "AdminDashboard/adminAddVehType.html", context)
    else:
        vob.save()
        messages.error(request, "Deleted Successfully")
        return HttpResponseRedirect('/admindash/ListVehicleType')


def ListVehicleType(request):
    vehicleobj = AddVehicle.objects.filter(isdeleted=False)
    return render(request, "AdminDashboard/adminAddVehType.html", {'vehicleobj': vehicleobj})


def EditProfile(request):
    return render(request, "AdminDashboard/adminEditProfile.html")


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
            return HttpResponseRedirect('/admindash/EditProfile')
        else:
            return render(request, "AdminDashboard/adminEditProfile.html", {'number': 'Invalid Number'})
    return render(request, "AdminDashboard/adminEditProfile.html")


def UpdatePassword(request):
    id = request.session['userid']
    if request.method == "POST":
        password = request.POST.get('newpassword')
        logobj = Login.objects.get(pk=id)
        logobj.password = make_password(password, salt=None, hasher='default')
        logobj.save()
        messages.success(request, "Password Changed Successfully")
        return HttpResponseRedirect('/admindash/EditProfile')
    return render(request, "AdminDashboard/adminEditProfile.html")


def SetRoute(request):
    location = AddLocations.objects.filter(isdeleted=False)
    routeob = AddRoute.objects.select_related().filter(isdeleted=False)
    if request.method == "POST":
        routname = request.POST.get('routename')
        sourcel = request.POST.get('slocation')
        destinationl = request.POST.get('dlocation')
        routeobj = AddRoute()
        routeobj.RouteName = routname
        sloc = AddLocations.objects.get(CityName=sourcel, isdeleted=False)
        dloc = AddLocations.objects.get(CityName=destinationl, isdeleted=False)
        routeobj.SourceLoc = sloc
        routeobj.DestinationLoc = dloc
        routeobj.isdeleted = False
        if AddRoute.objects.filter(RouteName=routname).filter(isdeleted=False).exists():
            messages.warning(request, "Already Exist!")
            return HttpResponseRedirect('/admindash/ListRoutes')
        elif sloc == dloc:
            messages.warning(request, "Same Location is not Possible")
            return HttpResponseRedirect('/admindash/ListRoutes')
        else:
            routeobj.save()
            messages.success(request, "Added Successfully")
            return HttpResponseRedirect('/admindash/ListRoutes')
    return render(request, "AdminDashboard/adminListRoute.html", {'location': location,'routeobj':routeob})


def EditRoute(request, pk):
    rob = AddRoute.objects.get(pk=pk)
    data = {
        'Id': rob.pk,
        'RouteName': rob.RouteName,
        'SourceLoc': rob.SourceLoc.CityName,
        'DestinationLoc': rob.DestinationLoc.CityName,
    }
    return JsonResponse(data)


def UpdateRoute(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('id')
        rname = request.POST.get('RouteName')
        sloc = request.POST.get('SourceLoc')
        dloc = request.POST.get('DestinationLoc')
        slocobj = AddLocations.objects.get(CityName=sloc, isdeleted=False)
        dlocobj = AddLocations.objects.get(CityName=dloc, isdeleted=False)
        robj = AddRoute.objects.get(pk=id)
        robj.RouteName = rname
        robj.SourceLoc = slocobj
        robj.DestinationLoc = dlocobj
        if AddRoute.objects.filter(RouteName=rname).filter(SourceLoc=slocobj.id).filter(DestinationLoc=dlocobj.id).filter(isdeleted=False).exists():
            message = {'error': "Already exists"}
            messages.warning(request, "Already Exists!")
            return JsonResponse(message)
        elif slocobj == dlocobj:
            message = {'error': "Already exists"}
            messages.warning(request, "Same Location is not Possible")
            return JsonResponse(message)
        else:
            robj.save()
            message = {'error': "Updated Successfully"}
            messages.success(request, "Updated Successfully")
            return JsonResponse(message)


def DeleteRoute(request, pk):
    rt = AddRoute.objects.get(pk=pk)
    rt.isdeleted = True
    if AddToll.objects.filter(RouteID=pk, isdeleted=False).exists():
        location = AddLocations.objects.filter(isdeleted=False)
        routeob = AddRoute.objects.select_related().filter(isdeleted=False)
        context = {
            'noroute': 'Can\'t Delete, Because there is an existing TollBooth in {}'.format(rt.RouteName),
            'routeobj': routeob, 'location': location,
        }
        return render(request, "AdminDashboard/adminListRoute.html", context)
    else:
        rt.save()
        messages.error(request, "Deleted Successfully")
        return HttpResponseRedirect('/admindash/ListRoutes')


def ListRoutes(request):
    location = AddLocations.objects.filter(isdeleted=False)
    routeob = AddRoute.objects.select_related().filter(isdeleted=False)
    return render(request, "AdminDashboard/adminListRoute.html", {'routeobj': routeob, 'location': location})


def AddTollBooths(request):
    tolls = AddToll.objects.select_related().filter(isdeleted=False)
    routes = AddRoute.objects.filter(isdeleted=False)
    if request.method == 'POST':
        tollname = request.POST.get('tollname')
        routename = request.POST.get('route')

        routeobject = AddRoute.objects.get(RouteName=routename)
        tolobject = AddToll()
        tolobject.TollName = tollname
        tolobject.RouteID = routeobject
        tolobject.isdeleted = False
        if AddToll.objects.filter(TollName=tollname, isdeleted=False).exists():
            messages.warning(request, "Already Exist!")
            return HttpResponseRedirect('/admindash/ListToll')
        else:
            tolobject.save()
            messages.success(request, "Added Successfully")
            return HttpResponseRedirect('/admindash/ListToll')
    return render(request, "AdminDashboard/adminListToll.html", {'routes':routes, 'tolls':tolls})


def EditTolls(request, pk):
    tob = AddToll.objects.get(pk=pk)
    data = {
        'Id': tob.pk,
        'TollName': tob.TollName,
        'RouteID': tob.RouteID.RouteName,
    }
    return JsonResponse(data)


def UpdateTolls(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('id')
        tname = request.POST.get('TollName')
        rloc = request.POST.get('RouteID')
        robj = AddRoute.objects.get(RouteName=rloc)
        tobj = AddToll.objects.get(pk=id)
        tobj.TollName = tname
        tobj.RouteID = robj
        if AddToll.objects.filter(TollName=tname).filter(RouteID=robj.id).filter(isdeleted=False).exists():
            message = {'error': "Already exists"}
            messages.warning(request, "Already Exists!")
            return JsonResponse(message)
        else:
            tobj.save()
            message = {'error': "Updated Successfully"}
            messages.success(request, "Updated Successfully")
            return JsonResponse(message)


def DeleteTolls(request, pk):
    tob = AddToll.objects.get(pk=pk)
    tob.isdeleted = True
    if AddPriceCharge.objects.filter(TollID=pk, isdeleted=False).exists():
        routes = AddRoute.objects.filter(isdeleted=False)
        tolls = AddToll.objects.select_related().filter(isdeleted=False)
        context = {
            'routes':routes, 'tolls': tolls,
            'notoll': 'Can\'t Delete, Because there is an existing data for the TollBooth {}'.format(tob.TollName),
        }
        return render(request, "AdminDashboard/adminListToll.html", context)
    else:
        tob.save()
        messages.error(request, "Deleted Successfully")
        return HttpResponseRedirect('/admindash/ListToll')


def ListTollBooths(request):
    routes = AddRoute.objects.filter(isdeleted=False)
    tolls = AddToll.objects.select_related().filter(isdeleted=False)
    return render(request, "AdminDashboard/adminListToll.html", {'routes':routes, 'tolls': tolls})


def SetCharges(request):
    if request.method == "POST":
        vehiclename = request.POST.get('vehtype')
        tollname = request.POST.get('tollnam')
        tobj = AddToll.objects.get(TollName=tollname, isdeleted=False)
        vobj = AddVehicle.objects.get(VehicleType=vehiclename, isdeleted=False)
        amount = request.POST.get('amount')

        ChargeObj = AddPriceCharge()
        ChargeObj.VehicleTypeID = vobj
        ChargeObj.TollID = tobj

        if AddPriceCharge.objects.filter(TollID=tobj.id).filter(VehicleTypeID=vobj.id).filter(isdeleted=False).exists():
            messages.warning(request, "Already Exists!")
            return HttpResponseRedirect('/admindash/ListCharge')
        else:
            ChargeObj.Amount = amount
            ChargeObj.save()
            messages.success(request, "Added Successfully")
            return HttpResponseRedirect('/admindash/ListCharge')


def EditCharge(request, pk):
    cob = AddPriceCharge.objects.get(pk=pk)
    data = {
        'Id': cob.pk,
        'VehicleTypeID': cob.VehicleTypeID.VehicleType,
        'TollID': cob.TollID.TollName,
        'Amount': cob.Amount
    }
    return JsonResponse(data)


def UpdateCharge(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('id')
        vname = request.POST.get('VehicleTypeID')
        tname = request.POST.get('TollID')
        amnt = request.POST.get('Amount')
        vobj = AddVehicle.objects.get(VehicleType=vname, isdeleted=False)
        tobj = AddToll.objects.get(TollName=tname, isdeleted=False)
        cobj = AddPriceCharge.objects.get(pk=id)
        cobj.VehicleTypeID = vobj
        cobj.TollID = tobj
        cobj.Amount = amnt
        if AddPriceCharge.objects.filter(TollID=tobj.id).filter(VehicleTypeID=vobj.id).filter(Amount=amnt).filter(isdeleted=False).exists():
            message = {'error': "Already exists"}
            messages.warning(request, "Already Exists!")
            return JsonResponse(message)
        else:
            cobj.save()
            message = {'error': "Updated Successfully"}
            messages.success(request, "Updated Successfully")
            return JsonResponse(message)


def DeleteCharge(request, pk):
    cob = AddPriceCharge.objects.get(pk=pk)
    cob.isdeleted = True
    if Booking.objects.filter(AmountID=pk, isCanceled=False, isExpired=False).exists():
        stoll = AddToll.objects.filter(isdeleted=False)
        vtype = AddVehicle.objects.filter(isdeleted=False)
        charge = AddPriceCharge.objects.select_related().filter(isdeleted=False)
        context = {
            'vtype':vtype, 'charge':charge, 'stoll': stoll,
            'nocharge': 'Can\'t Delete, Because there is an existing data for the amount Rs. {}'.format(cob.Amount),
        }
        return render(request, "AdminDashboard/adminSetCharge.html", context)
    else:
        cob.save()
        messages.error(request, "Deleted Successfully")
        return HttpResponseRedirect('/admindash/ListCharge')


def ListCharges(request):
    stoll = AddToll.objects.filter(isdeleted=False)
    vtype = AddVehicle.objects.filter(isdeleted=False)
    charge = AddPriceCharge.objects.select_related().filter(isdeleted=False)
    return render(request, "AdminDashboard/adminSetCharge.html", {'vtype':vtype, 'charge':charge, 'stoll': stoll})


def BookingHistory(request):
    return render(request, "AdminDashboard/adminBookingHistory.html")


