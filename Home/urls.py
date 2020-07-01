from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.Index, name="Index"),
    url(r'^register/', views.Register, name="Register"),
    url(r'^tollregister/', views.TollRegister, name="TollRegister"),
    url(r'^login/', views.LoggingIn, name="Login"),
    url(r'^allauthRegistration/', views.allauthRegistration, name='allauthRegistration'),
    url(r'^Forget/', views.ForgetPassword, name='forget'),
    url(r'^NewPass/', views.NewPass, name='NewPass'),
    url(r'^ForgetPass/',views.NewPassword, name='forgetpassword'),
]