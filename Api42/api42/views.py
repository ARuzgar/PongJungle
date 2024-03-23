import time
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from .serializers import *
import requests
import os, json, base64, io
from PIL import Image
from .models import BlacklistedToken
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
import subprocess


UID = "u-s4t2ud-272a7d972a922c63919b4411aff1da6abf64ec93eb38804b51427a0c0fbf86ea"
SECRET = "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"
REDIRECT_URI = "https://peng.com.tr/login/"


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


def blacklist_token(token):
    if not BlacklistedToken.objects.filter(token=token).exists():
        blacklisted_token = BlacklistedToken(token=token)
        blacklisted_token.save()


def list_blacklisted_tokens():
    blacklisted_tokens = BlacklistedToken.objects.all()
    for token in blacklisted_tokens:
        print(token.token)


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
                    JsonProviderBasic(
                        success="False",
                        message="42 API failed1",
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
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
                    "online_status": "True",
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
                        JsonProviderBasic(
                            success="True",
                            message="User registeration successfull",
                            data=new_data,
                        ),
                        status=status.HTTP_200_OK,
                    )
                else:
                    print("Validation errors:", serializer.error_messages)
                    return Response(
                        JsonProviderBasic(
                            success="False",
                            message=serializer.error_messages,
                        ),
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                refresh = RefreshToken.for_user(user)
                user.online_status = True
                user.save()
                data = {
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                }
            return Response(
                JsonProviderBasic(
                    success="True",
                    message="User registeration successfull",
                    data=data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            JsonProviderBasic(
                success="False",
                message="42 API failed",
            ),
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserRegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                JsonProviderBasic(
                    success="True",
                    message="User registeration successfull",
                ),
                status=status.HTTP_200_OK,
            )
        else:
            print("Validation errors:", serializer.error_messages)
            return Response(
                JsonProviderBasic(
                    success="False",
                    message=serializer.error_messages,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        if username is None or password is None:
            return Response(
                JsonProviderBasic(
                    success=False,
                    message="User informations missing",
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(username=username).first()
        if user is not None:
            user = authenticate(request, username=username, password=password)

            if BlacklistedToken.objects.filter(
                token=request.data.get("token")
            ).exists():
                return Response(
                    JsonProviderBasic(
                        success=False,
                        message="Token is blacklisted",
                    ),
                    status=status.HTTP_404_NOT_FOUND,
                )

            if user is not None:
                refresh = RefreshToken.for_user(user)
                data = {
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                }
                user.online_status = True
                user.save()
                return Response(
                    JsonProviderBasic(
                        success=True,
                        message="User login successfull",
                        data=data,
                    ),
                    status=status.HTTP_200_OK,
                )
            else:
                print("user login fail")
                return Response(
                    JsonProviderBasic(
                        success=False,
                        message="User login fail",
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            print("user not found")
            return Response(
                JsonProviderBasic(
                    success=False,
                    message="User not found",
                ),
                status=status.HTTP_400_BAD_REQUEST,
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
                JsonProviderBasic(
                    success=True,
                    message="User informations taken",
                    data=data,
                ),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                JsonProviderBasic(
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
            os.remove(image_path)
        with open(image_path, "wb") as file:
            for chunk in image_data.chunks():
                file.write(chunk)

    def put(self, request):
        user = User.objects.get(username=request.user.username)
        req_data = request.data.copy()
        type = req_data["type"]
        del req_data["type"]
        if user is not None:
            if (
                req_data["password"] != ""
                and make_password(req_data["password"]) != user.password
            ):
                user.password = make_password(req_data["password"])
            else:
                req_data["password"] = user.password
            if req_data["fullname"] != "" and req_data["fullname"] != user.fullname:
                user.fullname = req_data["fullname"]
            else:
                req_data["fullname"] = user.fullname
            if req_data["email"] != "" and req_data["email"] != user.email:
                user.email = req_data["email"]
            else:
                req_data["email"] = user.email
            user.ft_api_registered = user.ft_api_registered
            user.username = user.username

            if type != "":
                image_data = req_data["profile_picture"]
                print("profile picture taken: ", image_data)

                image_type = type
                image_path = "images/" + user.username + "." + image_type.split("/")[1]
                self.save_image_to_path(image_data, image_path)
                del req_data["profile_picture"]
                req_data["profile_picture"] = (
                    "/static/pofiles/image/" + image_path.split("/")[1]
                )
                user.profile_picture = (
                    "/static/pofiles/image/" + image_path.split("/")[1]
                )
            user.save()
            time.sleep(3)
            subprocess.run(["sh", "/cloudflare_cache_clear.sh"])
            print("req_data: ", req_data)
            # if serializer.is_valid():
            #     serializer.save()
            return Response(
                JsonProviderBasic(
                    success=True,
                    message="User data updated",
                ),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                JsonProviderBasic(
                    success=False,
                    message="User not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    # def save_image_to_path(self, image_data, image_path):
    #     if os.path.exists(image_path):
    #         os.remove(image_path)
    #     with open(image_path, "wb") as file:
    #         for (
    #             chunk
    #         ) in image_data.chunks():  # Assuming image_data is a Django File object
    #             file.write(chunk)

    # def create_data(self, user, data):
    #     created_data = {
    #         "username": user.username,
    #         "email": user.email,
    #         "fullname": user.fullname,
    #         "password": user.password,
    #         "ft_api_registered": user.ft_api_registered,
    #         "profile_picture": user.profile_picture,
    #     }
    #     for key, value in data.items():
    #         if value != "":
    #             created_data.update({key: value})
    #     if data["password"] != user.password and data["password"] != "":
    #         created_data["password"] = make_password(data["password"])
    #     return created_data

    # def post(self, request):
    #     user = User.objects.get(username=request.user.username)
    #     req_data = request.data
    #     print('#' * 20)
    #     print('req_data: ', request.data.get())
    #     if user is not None:

    #         if (req_data["password"] != "" and make_password(req_data["password"]) != user.password):
    #             req_data.update({"password": make_password(req_data["password"])})
    #         if req_data["fullname"] != "" and req_data["fullname"] != user.fullname:
    #             req_data.update({"fullname": req_data['fullname']})
    #         if req_data['email'] != "" and req_data["email"] != user.email:
    #             req_data.update({"email": req_data['email']})

    #         if type != "":
    #             image_data = req_data["profile_picture"]
    #             image_type = type
    #             image_path = "images/" + user.username + "." + image_type.split("/")[1]
    #             self.save_image_to_path(image_data, image_path)
    #             # del ready_data["profile_picture"]
    #             req_data.update(
    #                 {
    #                     "profile_picture": "/static/pofiles/image/"
    #                     + image_path.split("/")[1]
    #                 }
    #             )
    #         print('#' * 30)
    #         print('all req data: ', req_data)
    #         serializer = UserUpdateSerializer(
    #             instance=user, data=req_data, partial=True
    #         )
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(
    #                 JsonProviderBasic(
    #                     success=True,
    #                     message="User data updated",
    #                 ),
    #                 status=status.HTTP_200_OK,
    #             )
    #         else:
    #             print("error", serializer.error_messages)
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response(
    #             JsonProviderBasic(
    #                 success=False,
    #                 message="User not found",
    #             ),
    #             status=status.HTTP_404_NOT_FOUND,
    #         )


class UserLogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Kullanıcıyı bul
            user = request.user

            # Kullanıcının çevrimiçi durumunu false yap
            user.online_status = False
            user.save()

            refresh_token = request.data["refresh_token"]

            if refresh_token:
                blacklist_token(refresh_token)

            return Response(
                JsonProviderBasic(success=True, message="User logout successful"),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            # İşlem sırasında bir hata oluşursa
            return Response(
                JsonProviderBasic(
                    success=False, message="An error occurred while logging out."
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # def post(self, request):
    # print("#" * 20)
    # refresh_token = request.data["refresh_token"]
    # print("refresh_token: ", refresh_token)
    # user = User.objects.get(username=request.user.username)
    # user.online_status = False
    # user.save()
    # if refresh_token:
    #     refresh_token = RefreshToken(refresh_token)
    #     refresh_token.blacklist()


class UserCheckAPIView(APIView):

    def to_integer(self, dt_time):
        return 10000 * dt_time.year + 100 * dt_time.month + dt_time.day

    def post(self, request):
        if not request.auth:
            return Response(
                JsonProviderBasic(
                    success=False,
                    message="JWT tokeni bulunamadı.",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        token = request.auth
        token_str = str(token)

        if not BlacklistedToken.objects.filter(token=token_str).exists() and token[
            "exp"
        ] > self.to_integer(datetime.now()):
            return Response(
                JsonProviderBasic(
                    success=True,
                    message="Token geçerli.",
                ),
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                JsonProviderBasic(
                    success=False,
                    message="Token kara listede veya süresi geçmiş.",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )


# =========================== FRIENDSHIP APIs ===========================


class AddFriendAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        friend_username = request.data.get("friend_username")
        try:
            friend = User.objects.get(username=friend_username)
        except User.DoesNotExist:
            return Response(
                JsonProviderBasic(
                    success=False,
                    message="User not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        friendship = Friendship.objects.create(user1=user, user2=friend)

        return Response(
            JsonProviderBasic(
                success=True,
                message="Friendship done",
            ),
            status=status.HTTP_200_OK,
        )


class UserSearchAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get("query")
        if query:
            users = User.objects.filter(username__icontains=query)
            response_data = []
            for user in users:
                if (
                    user == request.user
                    or Friendship.objects.filter(
                        (
                            Q(user1=request.user, user2=user)
                            | Q(user1=user, user2=request.user)
                        )
                    ).exists()
                ):
                    continue

                serialized_data = {
                    "username": user.username,
                    "email": user.email,
                    "profile_picture": user.profile_picture,
                    "online_status": user.online_status,
                }
                response_data.append(serialized_data)

            return Response(
                JsonProviderBasic(
                    success=True,
                    message="successfull search",
                    data=response_data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            JsonProviderBasic(
                success=False,
                message="failed search",
            ),
            status=status.HTTP_404_NOT_FOUND,
        )


class CheckFriendshipAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, friend_username):
        user = request.user

        # Arkadaşın kullanıcı adı ile kullanıcıyı bul
        try:
            friend = User.objects.get(username=friend_username)
        except User.DoesNotExist:
            return Response(
                JsonProviderBasic(
                    success=False,
                    message="User not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        # Arkadaşlık ilişkisini kontrol et
        is_friends = Friendship.objects.filter(
            (Q(user1=user, user2=friend) | Q(user1=friend, user2=user))
        ).exists()

        return Response(
            {"is_friends": is_friends}
        )  # ===== == = = = = = = = == = = = = == = = = = == = = = = =


class FriendListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        friend_list = []
        friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
        for friendship in friendships:
            friend = friendship.user2 if friendship.user1 == user else friendship.user1
            print("friend: ", friend.username)
            serialized_data = {
                "username": friend.username,
                "email": friend.email,
                "profile_picture": friend.profile_picture,
                "online_status": friend.online_status,
            }
            friend_list.append(serialized_data)

        return Response(
            JsonProviderBasic(
                success=True,
                message="Successfull request",
                data=friend_list,
            ),
            status=status.HTTP_200_OK,
        )
