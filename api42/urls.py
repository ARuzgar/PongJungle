from django.urls import path
from .views import *
from backend.views import *

urlpatterns = [
    path("", UserLoginAPIView.as_view(), name="apilogin"),
    path('api/signup', UserSignUpAPIView.as_view(), name='apisignup'),
    path('api/login', UserLoginAPIView.as_view(), name='apilogin'),
    path('api/42auth/', User42AuthSignUpAPIView.as_view(), name='api42auth'),
    path("", HomePageView.as_view(), name="home"),
]
