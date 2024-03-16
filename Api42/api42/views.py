from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from rest_framework.serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.shortcuts import redirect
from rest_framework import status
from django.views import View
from .serializers import *
from urllib.parse import (
    urlparse,
    parse_qs
)
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
import requests, json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


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


@method_decorator(csrf_exempt, name='dispatch')
class UserLogoutAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        print("=*=" * 25)
        print(
            "logout view and user is authenticated: .ASDGASJDGK;SA: ",
            request.user.is_authenticated,
        )
        print("=*=" * 25)
        user = request.user
        # user = User.objects.filter(username=request.user.get_username()).first()
        print("ZATTIRI ZORT ZORT: ", self.request.user)
        print('#' * 20)
        print('melihin yarragi logoutdan once', request.session.get('melihinyarragi'))
        logout(request)
        print('melihin yarragi logoutdan sonra', request.session.get('melihinyarragi'))
        print('#' * 20)
        return Response(
            Providers.JsonProviderBasic(True, message="success logout"),
            status=HTTP_200_OK,
        )
        # else:
        #     return Response(
        #         Providers.JsonProviderBasic(False, message="fail logout"),
        #         status=HTTP_400_BAD_REQUEST,
            # )

@method_decorator(csrf_exempt, name='dispatch')
class UserLogDenemeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print('0000===0000 ' * 10 )
        print('request username: ', request.user)
        print('0000===0000 ' * 10 )
        return Response(
                Providers.JsonProviderBasic(True, message="null"),
                status=HTTP_200_OK,
            )

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print('ZATTIRI ZORT ZORT ZAAAARTTTTT', request.user)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
                    Providers.JsonProviderUserData(
                        'ademberke', 'ademberke@hotmail.com', "Success Login"
                    ),
                    status=HTTP_200_OK,
                )

@method_decorator(csrf_exempt, name='dispatch')
class User42LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        username = request.data.get("username")
        password = request.data.get("password")

        user = None

        if not username or not password:
            user = authenticate(request, token=request.query_params.get("token"))
            if user is not None:
                login(request, user)
                request.session['melihinyarragi'] = '40km'
                return Response(
                    Providers.JsonProviderUserData(
                        user.username, user.email, "Success Login"
                    ),
                    status=HTTP_200_OK,
                )
            # return HttpResponseRedirect('https://peng.com.tr/')
            return Response(
                Providers.JsonProviderBasic(True, message="failed login"),
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("-*-" * 20)
                print("-*-" * 20)
                login(request, user)
                print("request user logini control: ", request.user.username, request.user.is_authenticated, request.user.is_active)
                # return HttpResponseRedirect('https://peng.com.tr/')
                return Response(
                    Providers.JsonProviderUserData(
                        user.username, user.email, "Success Login"
                    ),
                    status=HTTP_200_OK,
                )
            else:
                if User.objects.filter().first() is None:
                    return Response(
                        Providers.JsonProviderBasic(True, message="user not found :/"),
                        status=HTTP_400_BAD_REQUEST,
                    )
                else:
                    return Response(
                        Providers.JsonProviderBasic(True, message="wrong password D:"),
                        status=HTTP_400_BAD_REQUEST,
                    )

@method_decorator(csrf_exempt, name='dispatch')
class SignUpAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        if username and email and password:
            existing_user = User.objects.filter(username=username).first()

            if existing_user is not None:
                return Response(
                    Providers.JsonProviderBasic(False, error="User already exist"),
                    status=HTTP_400_BAD_REQUEST,
                )

            data = {
                "email": email,
                "username": username,
                "password": password,
            }

            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                user = serializer.save()
                print("=*=" * 25)
                login(request, user)
                print("=*=" * 25)
                # token, created = Token.objects.get_or_create(user=user)
                print("signview", user.is_authenticated)
                return Response(
                    Providers.JsonProviderBasic(True, message="user registered"),
                    status=HTTP_200_OK,
                )
            else:
                return Response(
                    Providers.JsonProviderBasic(False, error="unknown failed"),
                    status=HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                Providers.JsonProviderBasic(
                    False, error="user informations are missing"
                ),
                status=HTTP_400_BAD_REQUEST,
            )

@method_decorator(csrf_exempt, name='dispatch')
class QueryUserData(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(username=request.user.username)
                print(user)
            except User.DoesNotExist:
                raise NotFound("User not found")
            return Response(
                Providers.JsonProviderUserData(
                    user.username, user.email, "Success Login"
                ),
                status=HTTP_200_OK,
            )
        else:
            return Response(
                Providers.JsonProviderBasic(False, message="not login"),
                status=HTTP_400_BAD_REQUEST,
            )

@method_decorator(csrf_exempt, name='dispatch')
class FtLoginAuthView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        code = request.data.get("code")
        if code:
            user_info = getUserInfo(code)
            if user_info and user_info["login"]:
                var = user_info["login"]
                existing_user = User.objects.filter(username=var).first()
                data = {
                    "username": user_info["login"],
                    "password": "pass",
                }
                if existing_user:
                    print("#" * 20)
                    print("   existing user   ")
                    print("#" * 20)
                    login(request, existing_user)
                    print("user authenticated?: ", request.user.is_authenticated)
                    print("user activate?: ", request.user.is_active)
                    return Response(
                        Providers.JsonProviderBasic(
                            True, data={"message": "logged in"}
                        ),
                        status=HTTP_200_OK,
                    )
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                    print("#" * 20)
                    print("  asdasd user   ")
                    print("#" * 20)
                    existing_user = User.objects.filter(username=var).first()
                    login(request, request.user)
                    print("user authenticated?: ", request.user.is_authenticated)
                    print("user activate?: ", request.user.is_active)
                    return Response(
                        Providers.JsonProviderBasic(
                            True, data={"message": "user registered"}
                        ),
                        status=HTTP_200_OK,
                    )
                return Response(
                    Providers.JsonProviderBasic(
                        False, error={"message": "serializer error"}
                    ),
                    status=HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(
                    Providers.JsonProviderBasic(
                        False, error={"message": "42 api error"}
                    ),
                    status=HTTP_400_BAD_REQUEST,
                )
                # After saving the user, make a POST request to UserLoginAPIView
                # login_response = requests.post('http://peng.com.tr/api42/api/login', data={'username': data['username'], 'password': data['password']})
                # if login_response.status_code == status.HTTP_200_OK:
                #     return HttpResponseRedirect(reverse('root'))
                # else:
                #     return JsonResponse({'error': 'Failed to login after signup.'}, status=400)
        return Response(
            Providers.JsonProviderBasic(
                False, error={"error": "Bad Request"}, status=HTTP_400_BAD_REQUEST
            )
        )


class AuthView(View):
    def get(self, request):
        return redirect(
            "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea&redirect_uri=https%3A%2F%2Fpeng.com.tr%2Fbackend%2F&response_type=code"
        )
