from django.urls import path
from .views import *
# from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('ft_auth/', FtLoginAuthView.as_view(), name='ftSignup'),
    path('login/', User42LoginAPIView.as_view(), name='login'),
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('signupa/', CustomAuthToken.as_view(), name='signupa'),
    path('ft_api/', AuthView.as_view(), name='apiStart'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('newlogin/', UserLoginView.as_view(), name='newlogin'),
    path('newsignup/', UserRegisterView.as_view(), name='newsignup'),
    path('query/user/', UserInfoQuery.as_view(), name='query_user'),
]