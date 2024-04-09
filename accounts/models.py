from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import Country, Currency


class User(AbstractUser):

    COUNTRY_CHOICES = [(c.value, c.name) for c in Country]
    CURRENCY_CHOICES = [(c.value, c.name) for c in Currency]

    email: str = models.EmailField(max_length=255, name="email")
    password: str = models.CharField(max_length=255, name="password")
    date_of_birth: date = models.DateField(
        name="date_of_birth", default=None, null=True, blank=True
    )
    country: str = models.CharField(
        max_length=len(max([c.value for c in Country], key=len)),
        choices=COUNTRY_CHOICES,
        null=True,
        blank=True,
    )
    currency: str = models.CharField(
        max_length=len(max([c.value for c in Currency], key=len)),
        choices=CURRENCY_CHOICES,
        null=True,
        blank=True,
    )
