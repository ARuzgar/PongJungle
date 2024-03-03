from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', User42AuthSignUpAPIView.as_view(), name='signup'),
    path('login/', User42LoginAPIView.as_view(), name='login'),
]