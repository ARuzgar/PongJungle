from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from rest_framework.permissions import AllowAny
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework.views import APIView
from backend.serializers import UserSerializer
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse_lazy
from backend.serializers import *
from django.contrib import messages
from rest_framework import generics
from rest_framework import status
from django.http import QueryDict
from django.urls import reverse
from django.views import View
import requests
import time
import json

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = None
        if not username or not password:
            user = authenticate(request, token=request.data['token'])
        else:
            user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('root'))
        else:
            return JsonResponse({'message': 'Gecersiz giris bilgileri.'}, status=400)