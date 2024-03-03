from django.urls import path
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    #path("auth/", AuthView.as_view(), name="auth"),
    path("callback", CallbackView.as_view(), name="callback"),
]
