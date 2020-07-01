from django.db import models
from AdminDashboard.models import *

# Home
class Login(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=264)
    roleid = models.IntegerField()
    isdeleted = models.BooleanField(default=False)
    isapproved = models.BooleanField(default=False)
    status = models.BooleanField(default=False)


class Registration(models.Model):
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    Address = models.CharField(max_length=264)
    Email = models.EmailField(max_length=50)
    Phone = models.CharField(max_length=12)
    Image = models.ImageField(upload_to='images/')


class TollRegisterAdditional(models.Model):
    workerid = models.ForeignKey(Registration, on_delete=models.CASCADE)
    Tollid = models.ForeignKey(AddToll, on_delete=models.CASCADE)
