from unicodedata import name

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email: str = models.EmailField(max_length=255, name="email")
    password: str = models.CharField(max_length=255, name="password")
