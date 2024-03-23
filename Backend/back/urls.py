from django.urls import path
from .views import *

urlpatterns = [
    path("match/", MatchCreateAndList.as_view(), name="match-create"),
]
