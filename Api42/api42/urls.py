from django.urls import path
from .views import *
# from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('ft_auth/', FtLoginAuthView.as_view(), name='ftSignup'),
    path('login/', User42LoginAPIView.as_view(), name='login'),
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('apistrt/', AuthView.as_view(), name='apiStart'),
]