from django.contrib.auth.models import AbstractUser
from django.db import models
from timezone_field import TimeZoneField


class User(AbstractUser):
    timezone = TimeZoneField(default='UTC')


class Profile(models.Model):
    pass
