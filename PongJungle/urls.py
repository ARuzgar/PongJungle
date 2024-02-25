from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('frontend.urls')),
    path('api/', include('api42.urls')),
    path('backend/', include('backend.urls')),
]
