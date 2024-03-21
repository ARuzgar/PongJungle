from django.urls import path
from .views import *
# from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('ft_auth/', UserFtRegisterView.as_view(), name='ftSignup'),
    path('ft_api/', AuthView.as_view(), name='apiStart'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('query/user/', UserInfoQuery.as_view(), name='query_user'),
    path('update/user/', UserUpdateView.as_view(), name='update_user'),
]
