from django.urls import path
from django.views.generic import TemplateView
#halledcez inş

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('', TemplateView.as_view(template_name='index.html'), name='root'),
]
