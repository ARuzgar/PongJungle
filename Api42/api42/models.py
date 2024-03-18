from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
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
