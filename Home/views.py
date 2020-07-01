from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from AdminDashboard.models import *
from django.contrib.auth.models import User
from .models import *
from . import forms
from django.contrib.auth.hashers import check_password, make_password
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
import datetime
from TollBooth import settings
import os


# Create your views here.
def Index(request):
    return render(request, 'Home/index.html')


def Register(request):
    formR = forms.RegisterForm()
    formL = forms.LoginForm()
    if request.method == 'POST':
        fname = request.POST.get('FirstName')
        lname = request.POST.get('LastName')
        addr = request.POST.get('Address')
        email = request.POST.get('Email')
        phone = request.POST.get('Phone')
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        formR = forms.RegisterForm(request.POST, request.FILES)
        formL = forms.LoginForm(request.POST)
        log = Login()
        log.username = uname
        log.password = make_password(pwd, salt=None, hasher='default')
        log.roleid = 3
        log.isdeleted = False
        log.isapproved = True
        log.status = True

        reg = Registration()
        reg.FirstName = fname
        reg.LastName = lname
        reg.Address = addr
        reg.Email = email
        reg.Phone = phone
        if phone.isdigit() and len(phone) == 10 or len(phone) == 12:
            if formR.is_valid() and formL.is_valid():
                log.save()
                reg.loginid = log
                reg.Image = formR.cleaned_data['Image']
                reg.save()
                return HttpResponseRedirect('/login')
            else:
                print("Error")
        else:
            context = {
                'formL': formL, 'formR': formR, 'number': 'Invalid Mobile Number'
            }
            return render(request, 'Home/Register.html', context)
    return render(request, 'Home/Register.html', {'formL': formL, 'formR': formR})


def TollRegister(request):
    formR = forms.RegisterForm()
    formL = forms.LoginForm()
    tollob = AddToll.objects.filter(isdeleted=False)
    if request.method == 'POST':
        fname = request.POST.get('FirstName')
        lname = request.POST.get('LastName')
        addr = request.POST.get('Address')
        email = request.POST.get('Email')
        phone = request.POST.get('Phone')
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        tollname = request.POST.get('tollname')
        tollobject = AddToll.objects.get(TollName=tollname, isdeleted=False)
        formR = forms.RegisterForm(request.POST, request.FILES)
        formL = forms.LoginForm(request.POST)
        log = Login()
        log.username = uname
        log.password = make_password(pwd, salt=None, hasher='default')
        log.roleid = 2
        log.isdeleted = False
        log.isapproved = False
        log.status = False

        reg = Registration()
        reg.FirstName = fname
        reg.LastName = lname
        reg.Address = addr
        reg.Email = email
        reg.Phone = phone

        tollreg = TollRegisterAdditional()
        tollreg.Tollid = tollobject
        if phone.isdigit() and len(phone) == 10 or len(phone) == 12:
            if formR.is_valid() and formL.is_valid():
                log.save()
                reg.loginid = log
                reg.Image = formR.cleaned_data['Image']
                reg.save()
                tollreg.workerid = reg
                tollreg.save()
                return HttpResponseRedirect('/login')
            else:
                print("Error")
        else:
            context = {
                'formL': formL, 'formR': formR, 'number': 'Invalid Mobile Number'
            }
            return render(request, 'Home/TollRegister.html', context)
    return render(request, 'Home/TollRegister.html', {'formL': formL, 'formR': formR, 'toll':tollob})


def allauthRegistration(request):
    obj = request.user
    print(obj.email)
    if Login.objects.filter(username=obj.username, isdeleted=False).exists():
        log = Login.objects.get(username=obj.username, isdeleted=False)
        formL = forms.LoginForm()
        context = {"error": "Already exist!. Sign in via username and password", "formL": formL}
        print(log)
        request.session["userid"] = log.id
        return HttpResponseRedirect('/Customers/Dashboard')
    else:
        log = Login()
        log.username = obj.username
        log.password = obj.password
        log.isdeleted = False
        log.roleid = 3
        log.isapproved = True
        log.status = True
        log.save()

        reg = Registration()
        reg.loginid = log
        reg.FirstName = obj.first_name
        reg.LastName = obj.last_name
        reg.Email = obj.email
        reg.Image = 'images/wp4683788-2019-joker-wallpapers_1WvBPlg.jpg'
        reg.Phone = "None"
        reg.Address = "None"
        reg.save()
        request.session["userid"] = log.id
    return HttpResponseRedirect('/Customers/Dashboard')


def NewPass(request):
    if request.method == 'POST':
        passwrd = request.POST.get('newpass')
        id = request.session['alluthid']
        name = request.session['alluthname']
        if Login.objects.filter(pk=id, username=name).exists():
            lob = Login.objects.get(pk=id)
            lob.password = make_password(passwrd, salt=None, hasher='default')
            lob.save()
        del request.session['alluthid']
        del request.session['alluthname']
        return HttpResponseRedirect('/login')
    return render(request, "Home/allauthPassword.html")


def LoggingIn(request):
    formL = forms.LoginForm()
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        if Login.objects.filter(username=uname).exists():
            user = Login.objects.get(username=uname)
            userdetails = Registration.objects.get(loginid=user.id)
            if check_password(pwd, user.password):
                if user.roleid == 1:
                    request.session["userid"] = user.id
                    return HttpResponseRedirect('/admindash/admindashboard')
                elif user.roleid == 2 and user.isapproved is True and user.isdeleted is False:
                    request.session["userid"] = user.id
                    workerdetails = TollRegisterAdditional.objects.get(workerid=userdetails.id)
                    workerobject = TollRegisterAdditional._meta.get_field('workerid')
                    workervalue = workerobject.value_from_object(workerdetails)
                    request.session["tollid"] = workervalue
                    return HttpResponseRedirect('/Workers/Dashboard')
                elif user.roleid == 3 and user.isdeleted is False:
                    request.session["userid"] = user.id
                    return HttpResponseRedirect('/Customers/Dashboard')
                else:
                    template = loader.get_template("Home/LoginIn.html")
                    context = {"error": "Invalid User!", "formL": formL}
                    return HttpResponse(template.render(context, request))
            else:
                template = loader.get_template("Home/LoginIn.html")
                context = {"error": "Incorrect Password!", "formL": formL}
                return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template("Home/LoginIn.html")
            context = {"error": "Invalid User!", "formL": formL}
            return HttpResponse(template.render(context, request))
    return render(request, 'Home/LoginIn.html', {'formL': formL})


def ForgetPassword(request):
    if request.method == 'POST':
        value = request.POST['unames']
        if Login.objects.filter(username=value).exists():
            lid = Login.objects.get(username=value)
            request.session["passid"] = lid.id
            Regobj = Registration.objects.get(loginid=lid.id)
            email = Regobj.Email
            context = {
                'details': Regobj,
            }
            subject, from_email, to = 'Request for password change', 'YOUR MAIL ID', str(email)
            text_content = 'Hi,' + Regobj.loginid.username + ', \nYour request for password change\nis under process. Click this link to reset: http://127.0.0.1:8000/ForgetPass/.\nRegard dN'
            html_content = render_to_string('Home/forgetpwdmail.html', context)
            mail = EmailMultiAlternatives(subject, text_content, from_email, [to])
            mail.attach_alternative(html_content, "text/html")
            mail.send()
            return HttpResponseRedirect('/login')
        return HttpResponse("Invalid user")
    return HttpResponseRedirect('/login')


def NewPassword(request):
    if request.method == 'POST':
        passwrd = request.POST.get('newpass')
        logid = request.session["passid"]
        lob = Login.objects.get(id=logid)
        lob.password = make_password(passwrd, salt=None, hasher='default')
        lob.save()
        return HttpResponseRedirect('/login')
    return render(request, "Home/ForgetPwd.html")


def Logout(request):
    if request.session['userid']:
        del request.session['userid']
    try:
        del request.session["tollid"]
    except:
        return HttpResponseRedirect('/login')
    return HttpResponseRedirect('/login')
