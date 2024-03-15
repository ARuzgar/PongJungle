import json
import requests
from django.shortcuts import render
from rest_framework.views import APIView, View
from rest_framework.response import Response
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect



# Create your views here.
def JsonProvider(success, **kwargs):
    d = {"success": success, "data": None, "error": None}
    if "data" in kwargs and kwargs["data"] is not None:
        d.update({"data": kwargs["data"]})
    elif "error" in kwargs and kwargs["error"] is not None:
        d.update({"error": kwargs["error"]})
    return json.dumps(d)


class HomeRedirectView(View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', None)
        if code:
            requests.post('https://peng.com.tr/api42/auth/ft_auth/', data={'code': code})
        return HttpResponseRedirect('https://peng.com.tr/')  # Burada yönlendirilecek URL'i belirtin