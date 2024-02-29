from django.urls import path
from .views import *
from .views import AuthView 
from api42.views import User42LoginAPIView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
	path("chat/", ChatPageView.as_view(), name="chat"),
    path("post/", PostCreateView.as_view(), name="postCreate"),
    path("list/", PostListView.as_view(), name="listView"),
    path("register/", UserCreateView.as_view(), name="createUser"),
    path('api/signup/', UserSignUpAPIView.as_view(), name='apisignup'),
    path('api/42login/', User42LoginAPIView.as_view(), name='api42login'),
    path('api/42auth/', User42AuthSignUpAPIView.as_view(), name='api42auth'),
    path("<int:pk>", UserDetailView.as_view(), name="userDetails"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("post/", PostCreateView.as_view(), name="post"),
    path("auth/", AuthView.as_view(), name="auth"),
    path("callback", CallbackView.as_view(), name="callback"),
]
