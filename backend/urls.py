from django.urls import path
from .views import *
from .views import AuthView 

urlpatterns = [
    path("", HomePageView.as_view(), name="root"),
    path("homeless", HomePageView.as_view(), name="homeless"),
	path("chat/", ChatPageView.as_view(), name="chat"),
    path("post/", PostCreateView.as_view(), name="postCreate"),
    path("list/", PostListView.as_view(), name="listView"),
    path("register/", UserCreateView.as_view(), name="createUser"),
    #path('api/login/', UserLoginAPIView.as_view(), name='api_login'),
    path('api/signup/', UserSignUpAPIView.as_view(), name='api_signup'),
    path("<int:pk>", UserDetailView.as_view(), name="userDetails"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("post/", PostCreateView.as_view(), name="post"),
    path("auth/", AuthView.as_view(), name="auth"),
    path("callback", CallbackView.as_view(), name="callback"),
]
