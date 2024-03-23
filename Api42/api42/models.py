from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class User(AbstractUser):

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        blank=False,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.CharField(
        _("email address"),
        max_length=128,
        unique=False,
        blank=False,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    password = models.CharField(
        _("password"),
        max_length=128,
        blank=False,
    )
    fullname = models.CharField(
        _("fullname"),
        max_length=250,
        help_text=_(
            "Required. 250 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    )
    profile_picture = models.CharField(
        _("profile picture"),
        max_length=300,
        default="/static/pofiles/image/Default Profile Picture.jpg"
    )
    ft_api_registered = models.BooleanField(
        _("ft_api_registered"),
        blank=False,
        default=False,
	)
    online_status = models.BooleanField(
        _("online_status"),
        blank=False,
        default=False,
    )


class Friendship(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friends')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friends_of')
    created_at = models.DateTimeField(auto_now_add=True)
    # Diğer alanlar eklenebilir, örneğin arkadaşlık durumu (onaylanmış, bekleyen vb.)



class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token