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
            print('User is authenticated')
        else:
            user = authenticate(request, username=username, password=password)
            print('User is NOT authenticated')
        if user is not None:
            login(request, user)
            print('User is logged in')
            print('[!!!]               normal loginden logged in olma durumu                  [!!!]')
            return HttpResponseRedirect(reverse('root'))
        else:
            return JsonResponse({'message': 'Gecersiz giris bilgileri.'}, status=400)

class User42LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        print('login apideyim')
        user = None
        if not username or not password:
            user = authenticate(request, token=request.data['token'])
            print('User is authenticated')
        else:
            user = authenticate(request, username=username, password=password)
            print('User is NOT authenticated')
        if user is not None:
            login(request, user)
            print('User is logged in')
            print('[!!!]               42 api loginden logged in olma durumu                  [!!!]')
            # return HttpResponseRedirect(reverse('root'))
            return Response({'message': 'Successfully logged in'}, status=status.HTTP_200_OK)
        else:
            # return JsonResponse({'message': 'Gecersiz giris bilgileri.'}, status=400)
            print('user none ve birseyler')
            login_response = requests.post('http://localhost:8000/api42/api/42login/', data={'data': data})

            if login_response.status_code == status.HTTP_200_OK:
                # Return a successful Response
                return Response({'message': 'Successfully logged in'}, status=status.HTTP_200_OK)
            else:
                # Return an error Response based on the external API response
                return Response({'message': 'Failed to log in', 'error_details': login_response.text}, status=login_response.status_code)