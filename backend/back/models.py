from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title
