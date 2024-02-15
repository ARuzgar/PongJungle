#!/usr/bin/env python3
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from rest_framework.permissions import AllowAny
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.response import Response
from django.urls import reverse_lazy
from .serializers import UserSerializer
from .models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from rest_framework import generics
from .serializers import UserSerializer
from django.views import View
import time
import requests
import json

UID = "u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea"
SECRET = "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"
REDIRECT_URI = "http://127.0.0.1:8000"

def get_access_token(code):
    url = "https://api.intra.42.fr/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": UID,
        "client_secret": SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve access token: {e}")
        return None

def get_user_info(access_token):
    url = "https://api.intra.42.fr/v2/me"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve user information: {e}")
        return None

def getUserInfo(auth_code):
    access_token = get_access_token(auth_code)
    if access_token:
        user_info = get_user_info(access_token)
        if user_info:
            print(user_info.get('login'))
            print(user_info.get('first_name'))
            print(user_info.get('last_name'))
            print(user_info.get('image'))
            return user_info
        else:
            return "Failed to retrieve user information."
    else:
        return "Failed to obtain access token."
        

class ChatPageView(TemplateView):
    template_name = 'blog/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_data'] = 'Bu veri home2.html içinde kullanılabilir.'
        return context

class HomePageView(TemplateView):
    template_name = "blog/index.html"    

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    def get(self, request, *args, **kwargs):

        code = request.GET.get('code', None)
        getUserInfo(code)
        return render(request, self.template_name, self.get_context_data())


class UserLoginView(LoginView):
    template_name = 'blog/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('/')


class UserLogoutView(LogoutView):
    template_name = 'blog/logout.html'
    redirect_authenticated_user = False
    success_url = reverse_lazy('/')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    success_url = '/post'
    fields = ['title', 'content', 'owner']
    template_name = 'blog/post.html'


class PostListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.all()
        else:
            return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context


class UserDetailView(DetailView):
	model = Post
	template_name = 'blog/details-user.html'
	context_object_name = 'user_details'

class UserCreateView(CreateView):
    model = User
    fields = ['username', 'password', 'email'] # 'is_active', 'is_staff'
    template_name = 'blog/user-register.html'
    success_url = '/'
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.set_password(form.cleaned_data['password'])
        obj.save()
        return super(UserCreateView, self).form_valid(form)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('root'))
        else:
            return JsonResponse({'message': 'Gecersiz giris bilgileri.'}, status=400)


class UserSignUpAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect(reverse('root'))
        else:
            error_messages = []
            for field_errors in serializer.errors.values():
                for error in field_errors:
                    error_messages.append(error)
            return JsonResponse({'error': 'Bad Request : ' + ' '.join(error_messages)}, status=400)


# ----------------- 42 API -----------------

# class AuthView(requests.View):
# 	#template_name = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea&redirect_uri=http%3A%2F%2F10.11.29.3%3A8000&response_type=code"
# 	def get(self, request):
#         # GET parametrelerini al
#         parametre1 = request.GET.get('parametre1', None)
#         parametre2 = request.GET.get('parametre2', None)

#         # Parametreleri kullanarak bir şeyler yap
#         cevap_metni = f'Parametre 1: {parametre1}, Parametre 2: {parametre2}'

#         return HttpResponse(cevap_metni)
#     # def get(request):
#         # Do any additional processing if needed
        
#         # Redirect the user to the specified URL
# 		# pass

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
    
class AuthView(View):
    def get(self, request):
        # istediğiniz URL'ye yönlendirme yapın
        return redirect('https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000&response_type=code')
    