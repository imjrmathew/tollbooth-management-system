from django.conf.urls import url
from django.urls import path
from . import views

app_name = "AdminDashboard"
urlpatterns = [
    path('admindashboard/', views.adminIndex, name="adminindex"),

    path('workerslist/', views.adminWorkersList, name="adminworkerslist"),
    path('ApproveWorkers/<int:id>', views.ApproveWorker, name="adminApproveWorker"),
    path('RejectWorkers/<int:id>', views.RejectWorker, name="adminRejectWorker"),

    path('customerslist/', views.adminCustomerList, name="admincustomerslist"),

    path('addDistrict/', views.AddDistricts, name="adminadddistrict"),
    path('addLocation/', views.AddLocation, name="adminaddlocation"),
    path('editLocation/<int:pk>', views.EditLocation, name="adminEditLocation"),
    path('updateLocation/', views.UpdateLocation, name="adminUpdateLocation"),
    path('deleteLocation/<int:pk>', views.DeleteLocation, name="adminDeleteLocation"),
    path('editDistrict/<int:pk>', views.EditDistrict, name="adminEditDistrict"),
    path('updateDistrict/', views.UpdateDistrict, name="adminUpdateDistrict"),
    path('deleteDistrict/<int:pk>', views.DeleteDistrict, name="adminDeleteDistrict"),
    path('ListDistrict/', views.ListDistrictsLocation, name="adminlistdistrictlocations"),

    path('ListVehicleType/', views.ListVehicleType, name="adminlistvehicletype"),
    path('AddVehicleType/', views.AddVehicleType, name="adminaddvehicletype"),
    path('EditVehicleTypes/<int:pk>', views.EditVehicleType, name="adminEditVehicleType"),
    path('UpdateVehicleTypes/', views.UpdateVehicleType, name="adminUpdateVehicleType"),
    path('DeleteVehicleTypes/<int:pk>', views.DeleteVehicleType, name="adminDeleteVehicleType"),

    path('EditProfile/', views.EditProfile, name="adminEditProfile"),
    path('UpdateProfile/', views.UpdateProfile, name="adminUpdateProfile"),
    path('UpdatePassword/', views.UpdatePassword, name="adminChangePassword"),

    path('ListRoutes/', views.ListRoutes, name="adminListRoute"),
    path('DeleteRoute/<int:pk>', views.DeleteRoute, name="adminDeleteRoute"),
    path('EditRoutes/<int:pk>', views.EditRoute, name="adminEditRoute"),
    path('UpdateRoutes/', views.UpdateRoute, name="adminUpdateRoute"),
    path('SetRoute/', views.SetRoute, name="adminSetRoute"),

    path('ListToll/', views.ListTollBooths, name="adminListToll"),
    path('SetToll/', views.AddTollBooths, name="adminSetToll"),
    path('EditToll/<int:pk>', views.EditTolls, name="adminEditToll"),
    path('UpdateToll/', views.UpdateTolls, name="adminUpdateToll"),
    path('DeleteToll/<int:pk>', views.DeleteTolls, name="adminDeleteToll"),

    path('ListCharge/', views.ListCharges, name="adminListCharge"),
    path('SetCharge/', views.SetCharges, name="adminSetCharge"),
    path('EditCharges/<int:pk>', views.EditCharge, name="adminEditCharge"),
    path('UpdateCharges/', views.UpdateCharge, name="adminUpdateCharge"),
    path('DeleteCharges/<int:pk>', views.DeleteCharge, name="adminDeleteCharge"),

    path('ListBooking/', views.BookingHistory, name="adminListBooking"),
]
