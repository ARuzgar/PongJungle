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
import requests, os, base64, time
import json
from django.contrib.auth.hashers import make_password


UID = "u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea"
SECRET = "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"
REDIRECT_URI = "https://peng.com.tr/login/"


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


class UserFtRegisterView(APIView):
    serializer_class = UserSerializer

    def getFtInformations(self, authentication_code):
        access_token_response = requests.post(
            "https://api.intra.42.fr/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": UID,
                "client_secret": SECRET,
                "code": authentication_code,
                "redirect_uri": REDIRECT_URI,
            },
        )

        access_token_response.raise_for_status()
        access_token = access_token_response.json().get("access_token")
        me_api_headers = {"Authorization": f"Bearer {access_token}"}
        me_api_response = requests.get(
            "https://api.intra.42.fr/v2/me", headers=me_api_headers
        ).json()

        return me_api_response

    def post(self, request):
        code = request.data.get("code")
        if code is not None:
            ft_user_informations = self.getFtInformations(code)
            if ft_user_informations is None:
                return Response(
                    Providers.JsonProviderBasic(
                        success="False",
                        message="42 API failed1",
                    ),
                    status=HTTP_400_BAD_REQUEST,
                )
            user = User.objects.filter(username=ft_user_informations["login"]).first()
            if user is None:  # user kayitli degilse
                print(ft_user_informations["image"]["link"])
                data = {
                    "username": ft_user_informations["login"],
                    "password": "pass",
                    "email": ft_user_informations["email"],
                    "fullname": ft_user_informations["usual_full_name"],
                    "profile_picture": ft_user_informations["image"]["link"],
                    "ft_api_registered": "True",
                }
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                    new_user = User.objects.filter(username=data["username"]).first()
                    refresh = RefreshToken.for_user(new_user)
                    new_data = {
                        "token": {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        },
                    }
                    return Response(
                        Providers.JsonProviderBasic(
                            success="True",
                            message="User registeration successfull",
                            data=new_data,
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
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                refresh = RefreshToken.for_user(user)
                data = {
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                }
            return Response(
                Providers.JsonProviderBasic(
                    success="True",
                    message="User registeration successfull",
                    data=data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            Providers.JsonProviderBasic(
                success="False",
                message="42 API failed",
            ),
            status=HTTP_400_BAD_REQUEST,
        )


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
        #  and user.ft_api_registered == 'False'
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
        if os.path.exists(image_path):
            print("#" * 20)
            print("image bulundu")
            print("#" * 20)
            os.remove(image_path)
        with open(image_path, "wb") as file:
            for (
                chunk
            ) in image_data.chunks():  # Assuming image_data is a Django File object
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
            if value != "":
                created_data.update({key: value})
        if data["password"] != user.password and data["password"] != "":
            created_data["password"] = make_password(data["password"])
        return created_data

    def put(self, request):
        user = User.objects.get(username=request.user.username)
        req_data = request.data.copy()
        type = req_data["type"]
        del req_data["type"]
        if user is not None:
            if req_data['password'] != '' and make_password(req_data['password']) != user.password:
                req_data.update({'password':make_password(req_data['password'])})
            if type != "":
                image_data = req_data["profile_picture"]
                image_type = type
                image_path = "images/" + user.username + "." + image_type.split("/")[1]
                self.save_image_to_path(image_data, image_path)
                # del ready_data["profile_picture"]
                req_data.update(
                    {
                        "profile_picture": "/static/pofiles/image/"
                        + image_path.split("/")[1]
                    }
                )
            serializer = UserUpdateSerializer(
                instance=user, data=req_data, partial=True
            )
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
                print("error", serializer.error_messages)
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
            "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea&redirect_uri=https%3A%2F%2Fpeng.com.tr%2Flogin%2F&response_type=code"
        )
