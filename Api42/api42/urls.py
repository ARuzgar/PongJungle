from django.urls import path
from .views import *
# from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('friend/list/', FriendListAPIView.as_view(), name='friend_list'),
    path('search/user/', UserSearchAPIView.as_view(), name='search_user'),
    path('update/user/', UserUpdateView.as_view(), name='update_user'),
    path('friend/add/', AddFriendAPIView.as_view(), name='friend_add'),
    path('ft_auth/', UserFtRegisterView.as_view(), name='ftSignup'),
    path('query/user/', UserInfoQuery.as_view(), name='query_user'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('signup/', UserRegisterView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
]
