from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeRedirectView.as_view(), name="home"),
    path("home/", HomeRedirectView.as_view(), name="homeRedirect"),
]
