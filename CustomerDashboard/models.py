from django.db import models
from AdminDashboard.models import *
from Home.models import Login


# Create your models here.
class VehicleReg(models.Model):
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    VehicleTypeID = models.ForeignKey(AddVehicle, on_delete=models.CASCADE)
    VehicleRegNum = models.CharField(max_length=15)
    isdeleted = models.BooleanField(default=False)


class Booking(models.Model):
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    TollID = models.ForeignKey(AddToll, on_delete=models.CASCADE)
    DateBooked = models.DateField(auto_now_add=False)
    TimeBooked = models.TimeField(auto_now_add=False, default="00:00:00")
    TimeExpired = models.TimeField(auto_now_add=False, default="00:00:00")
    DateExpired = models.DateField(auto_now_add=False)
    VehicleID = models.ForeignKey(VehicleReg, on_delete=models.CASCADE)
    AmountID = models.ForeignKey(AddPriceCharge, on_delete=models.CASCADE)
    isExpired = models.BooleanField(default=False)
    isCanceled = models.BooleanField(default=False)
