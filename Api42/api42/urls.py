from django.urls import path
from .views import *

urlpatterns = [
    path('ftsignup/', User42AuthSignUpAPIView.as_view(), name='ftsignup'),
    path('login/', User42LoginAPIView.as_view(), name='login'),
    path('signup/', SignUpAPIView.as_view(), name='signup'),
]