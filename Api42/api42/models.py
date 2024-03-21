from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import PIL


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
        blank=True,
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
        default="Default Profile Picture.jpg"
    )
    ft_api_registered = models.BooleanField(
        _("ft_api_registered"),
        blank=False,
        default=False,
	)
