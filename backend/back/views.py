#!/usr/bin/env python3
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate,login
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.urls import reverse
from django.views import View
from .serializers import UserSerializer
from .models import Post
import requests

class HomePageView(TemplateView):
    template_name = "../../frontend/templates/index.html"    

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', None)
        response = render(request, self.template_name, self.get_context_data())
        if code:
            requests.post('http://localhost:8000/backend/api/42auth/', data={'code': code})
        return response

class UserLoginView(LoginView):
    template_name = '../../frontend/templates/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('/')

class UserLogoutView(LogoutView):
    template_name = '../../frontend/templates/logout.html'
    redirect_authenticated_user = False
    success_url = reverse_lazy('/')

class UserSignUpAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        print('[!!!]   Request Get Element Type : ')
        data = {
            'username': request.data.get('username'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(reverse('root'))
        else:
            error_messages = []
            for field_errors in serializer.errors.values():
                for error in field_errors:
                    error_messages.append(error)
            return JsonResponse({'error': 'Bad Request : ' + ' '.join(error_messages)}, status=400)
        

class CallbackView(View):
    def get(self, request):
        # GET parametrelerini oku
        code = request.GET.get('code', None)
        # Parametreleri kullanarak bir şeyler yap
        # ...
        print('zart')
        print(code)
        print('zort')
        return HttpResponse('Success!')
