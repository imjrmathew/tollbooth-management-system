from django.urls import path
from . import views

app_name = "WorkersDashboard"
urlpatterns = [
    path('Dashboard/', views.index, name="workersIndex"),

    path('WokrersList/', views.WorkersLists, name="workersWorkersList"),

    path('ListRoute/', views.ListRoutes, name="workersListRoute"),

    path('ListTollBooth/', views.ListTollBooths, name="workersListTollBooth"),

    path('ListAmount/', views.ListAmounts, name="workersListAmount"),

    path('ListBooking/', views.BookingHistory, name="workersListBooking"),

    path('EditProfile/', views.EditProfile, name="workersEditProfile"),
    path('UpdateProfile/', views.UpdateProfile, name="workersUpdateProfile"),
    path('UpdatePassword/', views.UpdatePassword, name="workersChangePassword"),
    path('DeleteAccount/', views.DeleteAccount, name="workersDeleteAccount"),

    path('CheckStatus/', views.CheckStatus, name="CheckStatus"),
    path('SaveImage/', views.SaveImage, name="SaveImage"),

]