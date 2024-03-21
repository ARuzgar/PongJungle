from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.serializers import *
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from .serializers import *
import requests, os


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
                        Providers.JsonProviderBasic(
                            success="True",
                            message="User registeration successfull",
                            data=new_data,
                        ),
                        status=status.HTTP_200_OK,
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
                Providers.JsonProviderBasic(
                    success="True",
                    message="User registeration successfull",
                ),
                status=status.HTTP_200_OK,
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
                status=status.HTTP_400_BAD_REQUEST,
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
                    status=status.HTTP_200_OK,
                )
            else:
                print("user login fail")
                return Response(
                    Providers.JsonProviderBasic(
                        success=False,
                        message="User login fail",
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            print("user not found")
            return Response(
                Providers.JsonProviderBasic(
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
                Providers.JsonProviderBasic(
                    success=True,
                    message="User informations taken",
                    data=data,
                ),
                status=status.HTTP_200_OK,
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
            if (
                req_data["password"] != ""
                and make_password(req_data["password"]) != user.password
            ):
                req_data.update({"password": make_password(req_data["password"])})
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
        user = request.user
        user.online_status = False
        return Response(
            Providers.JsonProviderBasic(True, message="success logout"),
            status=status.HTTP_200_OK,
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
                Providers.JsonProviderBasic(
                    success=False,
                    message="User not found",
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        friendship = Friendship.objects.create(user1=user, user2=friend)

        return Response(
            Providers.JsonProviderBasic(
                success=True,
                message="Friendship done",
            ),
            status=status.HTTP_200_OK,
        )


class UserSearchAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get('query', 's')
        print('query', query)
        if query:
            users = User.objects.filter(username__icontains=query)
            serializer = UserSerializer(users, many=True)
            return Response(
                Providers.JsonProviderBasic(
                    success=True,
                    message="successfull search",
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            Providers.JsonProviderBasic(
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
                Providers.JsonProviderBasic(
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

        # Kullanıcının arkadaşlarını bul
        friends = User.objects.filter(
            id__in=Friendship.objects.filter(Q(user1=user) | Q(user2=user)).values_list(
                "user2", flat=True
            )
        )

        # Arkadaşların kullanıcı adlarını listele
        friend_usernames = [friend.username for friend in friends]

        return Response(
            Providers.JsonProviderBasic(
                success=True,
                message="Successfull request",
                data={"friend_list": friend_usernames},
            ),
            status=status.HTTP_200_OK,
        )
