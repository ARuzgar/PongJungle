import json
import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic.base import TemplateView


# Create your views here.
def JsonProvider(success, **kwargs):
    d = {"success": success, "data": None, "error": None}
    if "data" in kwargs and kwargs["data"] is not None:
        d.update({"data": kwargs["data"]})
    elif "error" in kwargs and kwargs["error"] is not None:
        d.update({"error": kwargs["error"]})
    return json.dumps(d)

class HomeRedirectView(TemplateView):
    template_name = "../../frontend/templates/index.html"

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', None)
        response = render(request, self.template_name, self.get_context_data())
        if code:
            requests.post('https://peng.com.tr/api42/auth/ft_auth/', data={'code': code})
        return response