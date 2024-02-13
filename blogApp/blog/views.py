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
from rest_framework.response import Response
from django.urls import reverse_lazy
from .serializers import UserSerializer
from .models import Post
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from rest_framework import generics
from .serializers import UserSerializer

class ChatPageView(TemplateView):
    template_name = 'blog/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_data'] = 'Bu veri home2.html içinde kullanılabilir.'
        return context

class HomePageView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
