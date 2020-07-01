from django.urls import path
from . import views

app_name = "CustomerDashboard"
urlpatterns = [
    path('Dashboard/', views.CustomerIndex, name="CustomerIndex"),

    path('ListVehicleReg/', views.ListVehicleReg, name="ListVehicleReg"),
    path('AddVehicleReg/', views.AddVehicleReg, name="AddVehicleReg"),
    path('EditVehicleReg/<int:pk>', views.EditVehicleReg, name="EditVehicleReg"),
    path('UpdateVehicleReg/', views.UpdateVehicleReg, name="UpdateVehicleReg"),
    path('DeleteVehicleReg/<int:pk>', views.DeleteVehicleReg, name="DeleteVehicleReg"),

    path('Booking/', views.BookNow, name="Booking"),
    path('Checkout/', views.Checkout, name="Checkout"),
    path('EditBooking/<int:pk>', views.EditBooking, name="EditBooking"),
    path('UpdateBooking/', views.UpdateBooking, name="UpdateBooking"),
    path('CancelBooking/', views.CancelBooking, name="CancelBooking"),
    path('ListBooking/', views.ListBooking, name="ListBooking"),

    path('GetRegValue/<int:pk>', views.GetRegValue, name="GetRegValue"),
    path('GetTollValue/<str:pk>', views.GetTollValue, name="GetTollValue"),
    path('GetExpiry/<str:pk>', views.GetExpiry, name="GetExpiry"),

    path('UpdateProfile/', views.UpdateProfile, name="CustomerUpdateProfile"),
    path('UpdatePassword/', views.UpdatePassword, name="CustomerChangePassword"),
    path('DeleteAccount/', views.DeleteAccount, name="CustomerDeleteAccount"),
]