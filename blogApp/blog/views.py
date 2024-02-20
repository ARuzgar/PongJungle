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
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from rest_framework import generics
from rest_framework import status
from django.http import QueryDict
from django.urls import reverse
from django.views import View
from .models import Post
import requests
import time
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
        response = render(request, self.template_name, self.get_context_data())
        if code:
            requests.post('http://localhost:8000/api/signup/', data={'token': code})
        return response

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

class UserSignUpAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        if request.data['token']:
            user_info = getUserInfo(request.data['token'])
            if user_info:
                if not user_info['login'].strip():
                    return JsonResponse({'error': 'User login is empty or contains only whitespace.'}, status=400)
                print(User.objects.filter(username__iexact=user_info['login'].strip()).query)
                
                login_info = user_info['login'] + '42'
                
                existing_username = User.objects.filter(username__iexact=user_info['login'].strip()).exists()
                existing_email = User.objects.filter(email__iexact=user_info['email'].strip()).exists()
                
                if existing_username or existing_email:
                    
                    request.session['signup_username'] = user_info['login'].strip()
                    request.session['signup_email'] = user_info['email'].strip()
                    
                    print("User already exists. Redirecting to login page.")
                    return HttpResponseRedirect(reverse('api_login'))
                
                quer_dict = QueryDict('', mutable=True)
                quer_dict.appendlist('username', login_info)
                quer_dict.appendlist('email', user_info['email'])
                quer_dict.appendlist('password', login_info)
            else:
                return JsonResponse({'error': 'Failed to retrieve user information.'}, status=400)
        else:
            quer_dict = QueryDict('', mutable=True)
            quer_dict.appendlist('username', request.data.get('login'))
            quer_dict.appendlist('email', request.data.get('email'))
            quer_dict.appendlist('password', request.data.get('password'))

        serializer = self.serializer_class(data=quer_dict)

        if serializer.is_valid():
            print('-	-	-	-	Signup done	-	-	-	-')
            serializer.save()
            return HttpResponseRedirect(reverse('root'))
        else:
            error_messages = []
            for field_errors in serializer.errors.values():
                for error in field_errors:
                    error_messages.append(error)
            print('-	-	-	-	Signup ERRORRR	-	-	-	-')
            print(serializer.errors)
            print(quer_dict)
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
        print(code)
        return HttpResponse('Success!')
    
class AuthView(View):
    def get(self, request):
        # istediğiniz URL'ye yönlendirme yapın
        return redirect('https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000&response_type=code')
    