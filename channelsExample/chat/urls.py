from django.urls import path
from chat.views import ChatPageView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", ChatPageView.as_view(), name="chat-page"),
    path("auth/login/", LoginView.as_view(template_name="LoginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]
