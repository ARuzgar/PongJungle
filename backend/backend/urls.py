from django.urls import path, include

urlpatterns = [
    path('backend/', include('back.urls')),
]
