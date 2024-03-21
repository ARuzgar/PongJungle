from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from rest_framework.serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.renderers import JSONRenderer
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from django.core.files.base import ContentFile
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
from urllib.parse import urlparse, parse_qs
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
import requests, os, base64
import json
from django.contrib.auth.hashers import make_password



UID = "u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea"
SECRET = "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"
REDIRECT_URI = "https://peng.com.tr/backend/"




# def get_access_token(code):
#     url = "https://api.intra.42.fr/oauth/token"
#     payload = {
#         "grant_type": "authorization_code",
#         "client_id": UID,
#         "client_secret": SECRET,
#         "code": code,
#         "redirect_uri": REDIRECT_URI,
#     }
#     try:
#         response = requests.post(url, data=payload)
#         response.raise_for_status()
#         return response.json().get("access_token")
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to retrieve access token: {e}")
#         return None


# def get_user_info(access_token):
#     url = "https://api.intra.42.fr/v2/me"
#     headers = {"Authorization": f"Bearer {access_token}"}
#     try:
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to retrieve user information: {e}") 
#         return None


# def getUserInfo(auth_code):
#     access_token = get_access_token(auth_code)
#     if access_token:
#         user_info = get_user_info(access_token)
#         if user_info:
#             return user_info
#         else:
#             raise Exception("Failed to retrieve user information.")
#     else:
#         raise Exception("Failed to obtain access token.")


class Providers:
    def JsonProviderBasic(success, message, **kwargs):
        d = {
            "success": success,
            "data": None,
            "message": message,
            "error": None,
        }
        if "data" in kwargs and kwargs["data"] is not None:
            d.update({"data": kwargs["data"]})
        if "error" in kwargs and kwargs["error"] is not None:
            d.update({"error": kwargs["error"]})
        return d

    def JsonProviderUserData(success, message, data, **kwargs):
        d = {
            "success": success,
            "data": data,
            "message": message,
            "error": None,
        }
        if "error" in kwargs and kwargs["error"] is not None:
            d.update({"error": kwargs["error"]})
        return d


# =========================== NEW DRF APIs ===========================
@method_decorator(csrf_exempt, name="dispatch")
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

class UserFtRegisterView(APIView):
    
    def getFtInformations(self, authentication_code):
        access_token_response = requests.post("https://api.intra.42.fr/oauth/token", data = {
        	"grant_type": "authorization_code",
        	"client_id": UID,
        	"client_secret": SECRET,
        	"code": authentication_code,
        	"redirect_uri": REDIRECT_URI
        })

        access_token_response.raise_for_status()
        access_token = access_token_response.json().get("access_token")
        me_api_headers = {"Authorization": f"Bearer {access_token}"}
        me_api_response = requests.get("https://api.intra.42.fr/v2/me", headers=me_api_headers).json()

        print('#', 10)
        print("userdata: ", me_api_response)
        print('#', 10)
        return me_api_response
    
    def post(self, request):
        code = request.data.get("code")
        if code is not None:
            ft_user_informations = self.getFtInformations(code)
            if ft_user_informations is None:
                return
            user = User.objects.filter(username=ft_user_informations['login']).first()
            if user is None:
                data = {
					'username':ft_user_informations['login'],
					'password':'pass',
					'email':ft_user_informations['asd@asd.com'],
					'fullname':ft_user_informations['login'],
					'profile_picture':'asd.png',
					'is_ft_registered':True,
				}
                return Response(Providers.JsonProviderBasic(
                    success="False",
                    message="42 API failed",
                ),
                status=HTTP_400_BAD_REQUEST,
            )
            
        return Response()

class UserRegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                Providers.JsonProviderBasic(
                    success="True",
                    message="User registeration successfull",
                ),
                status=HTTP_200_OK,
            )
        else:
            print("Validation errors:", serializer.error_messages)
            return Response(
                Providers.JsonProviderBasic(
                    success="False",
                    message=serializer.error_messages,
                ),
                status=HTTP_400_BAD_REQUEST,
            )


class UserLoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        if username is None or password is None:
            return Response(
                Providers.JsonProviderBasic(
                    success=False,
                    message="User informations missing",
                ),
                status=HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(username=username).first()

        if user is not None:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                data = {
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                }
                return Response(
                    Providers.JsonProviderBasic(
                        success=True,
                        message="User login successfull",
                        data=data,
                    ),
                    status=HTTP_200_OK,
                )
            else:
                print("user login fail")
                return Response(
                    Providers.JsonProviderBasic(
                        success=False,
                        message="User login fail",
                    ),
                    status=HTTP_400_BAD_REQUEST,
                )
        else:
            print("user not found")
            return Response(
                Providers.JsonProviderBasic(
                    success=False,
                    message="User not found",
                ),
                status=HTTP_400_BAD_REQUEST,
            )


class UserInfoQuery(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        if user is not None:

            # PROFILE PHOTO EKLEMEYI UNUTMA
            print("#" * 20)
            path = str(user.profile_picture)
            data = {
                "username": user.username,
                "email": user.email,
                "profile_picture": path,
            }
            return Response(
                Providers.JsonProviderBasic(
                    success=True,
                    message="User informations taken",
                    data=data,
                ),
                status=HTTP_200_OK,
            )
        else:
            return Response(
                Providers.JsonProviderBasic(
                    success=False,
                    message="User not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )


class UserUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def save_image_to_path(self, image_data, image_path):
        with open(image_path, "wb") as file:
            for chunk in image_data.chunks():
                file.write(chunk)

    def create_data(self, user, data):
        created_data = {
            "username": user.username,
            "email": user.email,
            "fullname": user.fullname,
            "password": user.password,
            "ft_api_registered": user.ft_api_registered,
            "profile_picture": user.profile_picture,
        }
        for key, value in data.items():
            if value != '':
                created_data.update({key:value})
        if data["password"] != user.password and data["password"] != '':
            created_data["password"] = make_password(data["password"])
        return created_data

    def put(self, request):
        user = User.objects.get(username=request.user.username)
        req_data = request.data.copy()
        type = req_data["type"]
        print('type', req_data["type"])
        del req_data["type"]
        print(req_data)
        if user is not None:
            ready_data = self.create_data(user, req_data)
            if type != '':
                image_data = ready_data["profile_picture"]
                image_type = type
                image_path = "images/" + user.username + "." + image_type.split("/")[1]
                self.save_image_to_path(image_data, image_path)
                # del ready_data["profile_picture"]
                ready_data.update({"profile_picture": image_path.split("/")[1]})


            serializer = UserSerializer(
                user,
                data=ready_data,
                partial=True,
            )

            print('initial_data', serializer.initial_data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    Providers.JsonProviderBasic(
                        success=True,
                        message="User data updated",
                    ),
                    status=status.HTTP_200_OK,
                )
            else:
                print('error', serializer.error_messages)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                Providers.JsonProviderBasic(
                    success=False,
                    message="User not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )


# ====================================================================


@method_decorator(csrf_exempt, name="dispatch")
class UserLogoutAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        return Response(
            Providers.JsonProviderBasic(True, message="success logout"),
            status=HTTP_200_OK,
        )




class AuthView(View):
    def get(self, request):
        return redirect(
            "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea&redirect_uri=https%3A%2F%2Fpeng.com.tr%2Fbackend%2F&response_type=code"
        )
