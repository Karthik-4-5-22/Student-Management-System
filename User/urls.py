from django.urls import path
from . import views

urlpatterns = [
    path("",views.check,name="Check"),
    path("login/", views.user_login,name="Login"),
    path("details/",views.details,name="Details"),
    path("logout/",views.user_logout,name="Logout")
]
