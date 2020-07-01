from django.db import models

# Create your models here.


class AddDistrict(models.Model):
    DistrictName = models.CharField(max_length=256)
    isdeleted = models.BooleanField(default=False)


class AddLocations(models.Model):
    CityName = models.CharField(max_length=256)
    DistrictId = models.ForeignKey(AddDistrict, on_delete=models.CASCADE)
    isdeleted = models.BooleanField(default=False)


class AddRoute(models.Model):
    RouteName = models.CharField(max_length=256)
    SourceLoc = models.ForeignKey(AddLocations, on_delete=models.CASCADE, related_name='SourceLoc')
    DestinationLoc = models.ForeignKey(AddLocations, on_delete=models.CASCADE, related_name='DestinationLoc')
    isdeleted = models.BooleanField(default=False)


class AddToll(models.Model):
    TollName = models.CharField(max_length=256)
    RouteID = models.ForeignKey(AddRoute, on_delete=models.CASCADE)
    isdeleted = models.BooleanField(default=False)


class AddVehicle(models.Model):
    VehicleType = models.CharField(max_length=30)
    isdeleted = models.BooleanField(default=False)


class AddPriceCharge(models.Model):
    Amount = models.IntegerField()
    TollID = models.ForeignKey(AddToll, on_delete=models.CASCADE)
    VehicleTypeID = models.ForeignKey(AddVehicle, on_delete=models.CASCADE)
    isdeleted = models.BooleanField(default=False)

