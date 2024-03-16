import json
import requests
from django.shortcuts import render
from rest_framework.views import APIView, View
from rest_framework.response import Response
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect




class Providers:
    def JsonProviderBasic(success, **kwargs):
        d = {
            "success": success,
            "message": None,
            "error": None,
        }
        if "message" in kwargs and kwargs["message"] is not None:
            d.update({"message": kwargs["message"]})
            return d
        elif "error" in kwargs and kwargs["error"] is not None:
            d.update({"error": kwargs["error"]})
            return d

    def JsonProviderUserData(username, email, message, **kwargs):
        d = {
            "message": message,
            "username": username,
            "email": email,
            "phone": None,
            "photo": None,
        }
        if "photo" in kwargs and "phone" in kwargs:
            d.update({"photo": kwargs["photo"]})
            d.update({"phone": kwargs["phone"]})
        return d


class HomeRedirectView(View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', None)
        if code:
            requests.post('https://peng.com.tr/api42/auth/ft_auth/', data={'code': code})
        return HttpResponseRedirect('https://peng.com.tr/')
    