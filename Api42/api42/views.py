from rest_framework.authtoken.views import ObtainAuthToken
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
from urllib.parse import urlparse, parse_qs
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
import requests, os
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


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



# 
# class save_png_file(APIView):
#     def get(self, request):
#         if request.FILES.get('profile_picture'):
#             uploaded_file = request.FILES['profile_picture']
#             upload_path = os.path.join('./images')
#             os.makedirs(upload_path, exist_ok=True)
#             with open(os.path.join(upload_path, uploaded_file.name), 'wb+') as destination:
#                 for chunk in uploaded_file.chunks():
#                     destination.write(chunk)

# =========================== NEW DRF APIs ===========================


class UserRegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        print("#" * 20)
        print(request.data["username"])
        print(request.data["fullname"])
        print(request.data["email"])
        print("#" * 20)

        serializer = self.serializer_class(data=request.data)

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

        print(username, ' ', password)
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
            print("user logi nfailedededed")
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
            print('#' * 20)
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


class UpdateProfilePictureView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        picture_url = request.data.get("picture_url")

        if not picture_url:
            return Response(
                {"error": "Picture URL is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user.profile_picture = picture_url
        user.save()

        serializer = UserSerializer(user)

        return Response(
            Providers.JsonProviderBasic(
                success="True",
                message="User registeration successfull",
            ),
            status=HTTP_200_OK,
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


@method_decorator(csrf_exempt, name="dispatch")
class UserLogDenemeAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response(
            Providers.JsonProviderBasic(True, message="null"),
            status=HTTP_200_OK,
        )


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print("ZATTIRI ZORT ZORT ZAAAARTTTTT", request.user)
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            Providers.JsonProviderUserData(
                "ademberke", "ademberke@hotmail.com", "Success Login"
            ),
            status=HTTP_200_OK,
        )


@method_decorator(csrf_exempt, name="dispatch")
class User42LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        username = request.data.get("username")
        password = request.data.get("password")

        user = None

        print("*" * 50)
        token = 1234
        print(f"{username}, {password}, {token}")
        print("*" * 50)
        return Response(
            Providers.JsonProviderBasic(
                True, message={"token": token, "username": username}
            ),
            status=HTTP_200_OK,
        )


@method_decorator(csrf_exempt, name="dispatch")
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


@method_decorator(csrf_exempt, name="dispatch")
class QueryUserData(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        print("*" * 50)
        print(request.user)
        print("*" * 50)
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


class AuthView(View):
    def get(self, request):
        return redirect(
            "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea&redirect_uri=https%3A%2F%2Fpeng.com.tr%2Fbackend%2F&response_type=code"
        )
