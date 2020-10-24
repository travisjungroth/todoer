from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_token = models.CharField(default='', blank=True, max_length=255)
