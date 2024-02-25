from django.urls import path
from .views import *

urlpatterns = [
    path("", UserLoginAPIView.as_view(), name="apilogin"),
]

