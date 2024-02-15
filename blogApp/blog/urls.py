from django.urls import path
from .views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="root"),
<<<<<<< HEAD
    path("home", HomePageView.as_view(), name="home"),
=======
    path("homeless", HomePageView.as_view(), name="homeless"),
>>>>>>> 3500f072a33d771e490297253bfc4c7688ce36a1
	path("chat/", ChatPageView.as_view(), name="chat"),
    path("post/", PostCreateView.as_view(), name="postCreate"),
    path("list/", PostListView.as_view(), name="listView"),
    path("register/", UserCreateView.as_view(), name="createUser"),
    path('api/login/', UserLoginAPIView.as_view(), name='api_login'),
    path('api/signup/', UserSignUpAPIView.as_view(), name='api_signup'),
    path("<int:pk>", UserDetailView.as_view(), name="userDetails"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("post/", PostCreateView.as_view(), name="post"),
<<<<<<< HEAD
=======
    path("auth/", AuthView.as_view(), name="auth"),
    path("callback", CallbackView.as_view(), name="callback"),
>>>>>>> 3500f072a33d771e490297253bfc4c7688ce36a1
]
