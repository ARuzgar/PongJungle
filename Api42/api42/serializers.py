from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User
from .models import Friendship


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "fullname",
            "profile_picture",
            "ft_api_registered",
            "online_status",
        )
        extra_kwargs = {
            "username": {"write_only": True},
            "password": {"write_only": True},
            "fullname": {"required": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "fullname",
            "profile_picture",
            "ft_api_registered",
        )
        extra_kwargs = {
            "username": {"required": False},
            "password": {"required": False},
            "fullname": {"required": False},
            "email": {"required": False},
            "profile_picture": {"required": False},
            "ft_api_registered": {"required": False},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.get("password")
        if password is not None:  # Şifre değişikliği istenmişse
            validated_data["password"] = make_password(password)
        user = User.objects.create_user(**validated_data)
        return user


# ============================= FRIENDSHIP SERIALIZERS =============================


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = "__all__"


class AddFriendSerializer(serializers.Serializer):
    friend_username = serializers.CharField()


class CheckFriendshipSerializer(serializers.Serializer):
    friend_username = serializers.CharField()


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "fullname",
            "profile_picture",
            "ft_api_registered",
            "online_status",
        )
