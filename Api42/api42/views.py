from rest_framework.serializers import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import *
from rest_framework import status
from django.urls import reverse
from django.views import View
import json
from django.http import JsonResponse
import requests


from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


from urllib.parse import urlparse, parse_qs

UID = "u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea"
SECRET = "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"
REDIRECT_URI = "https://peng.com.tr/backend/"


def get_access_token(code):
    url = "https://api.intra.42.fr/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": UID,
        "client_secret": SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
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
    headers = {"Authorization": f"Bearer {access_token}"}
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


def JsonProvider(success, **kwargs):
    d = {"success": success, "message": None, "error": None}
    if "message" in kwargs and kwargs["message"] is not None:
        d.update({"message": kwargs["message"]})
        return d
    elif "error" in kwargs and kwargs["error"] is not None:
        d.update({"error": kwargs["error"]})
        return d


class User42LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        username = request.data.get("username")
        password = request.data.get("password")

        user = None
        if not username or not password:
            user = authenticate(request, token=request.query_params.get("token"))
            if user is not None:
                return Response(
                    JsonProvider(True, message="success login :D"),
                    status=HTTP_200_OK,
                )
            return Response(
                JsonProvider(True, data={"message": "failed login"}),
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return Response(
                    JsonProvider(True, message="success login :D"),
                    status=HTTP_200_OK,
                )
            else:
                return Response(
                    JsonProvider(True, data={"message": "failed login"}),
                    status=HTTP_400_BAD_REQUEST,
                )


class SignUpAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if username and email and password:
            existing_user = User.objects.filter(username=username).first()

            if existing_user is not None:
                return Response(
                    JsonProvider(False, error={"message": "user already exist"}),
                    status=HTTP_400_BAD_REQUEST,
                )

            data = {
                "email": email,
                "username": username,
                "password": password,
            }

            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    JsonProvider(True, data="user registered"),
                    status=HTTP_200_OK,
                )
            else:
                return Response(
                    JsonProvider(False, error="unknown failed"),
                    status=HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                JsonProvider(False, error="user informations are missing"),
                status=HTTP_400_BAD_REQUEST,
            )


class FtLoginAuthView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        code = request.data.get("code")
        if code:
            user_info = getUserInfo(code)
            print(user_info)
            if user_info and user_info["login"]:
                var = user_info["login"]
                existing_user = User.objects.filter(username=var).first()
                data = {
                    "username": user_info["login"],
                    "password": "pass",
                }
                if existing_user:
                    login(request, existing_user)
                    return Response(
                        JsonProvider(True, data={"message": "logged in"}),
                        status=HTTP_200_OK,
                    )
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                    # login(request, self.user)
                    return Response(
                        JsonProvider(True, data={"message": "user registered"}),
                        status=HTTP_200_OK,
                    )
                return Response(
                    JsonProvider(False, error={"message": "serializer error"}),
                    status=HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(
                    JsonProvider(False, error={"message": "42 api error"}),
                    status=HTTP_400_BAD_REQUEST,
                )
                # After saving the user, make a POST request to UserLoginAPIView
                # login_response = requests.post('http://peng.com.tr/api42/api/login', data={'username': data['username'], 'password': data['password']})
                # if login_response.status_code == status.HTTP_200_OK:
                #     return HttpResponseRedirect(reverse('root'))
                # else:
                #     return JsonResponse({'error': 'Failed to login after signup.'}, status=400)
        return Response(
            JsonProvider(
                False, error={"error": "Bad Request"}, status=HTTP_400_BAD_REQUEST
            )
        )


class AuthView(View):
    def get(self, request):
        return redirect(
            "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea&redirect_uri=https%3A%2F%2Fpeng.com.tr%2Fbackend%2F&response_type=code"
        )
