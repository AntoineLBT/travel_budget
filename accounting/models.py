import random
import string
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from django.db import models
from django.db.models import CheckConstraint, F, Q, Sum
from django.template.defaultfilters import slugify
from django.utils import timezone

from accounts.models import User

from .constants import Category


@dataclass
class Token:
    token: str
    expiry: datetime


class Trip(models.Model):
    id: UUID = models.UUIDField(primary_key=True, default=uuid4)
    name: str = models.CharField(
        name="name",
        max_length=255,
    )
    description: str = models.TextField(name="description", max_length=1023, default="")
    start_date: date = models.DateField(name="start_date")
    end_date: date = models.DateField(name="end_date")
    owner: User = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, related_name="trip_owner"
    )
    members: User = models.ManyToManyField(User)
    budget = models.DecimalField(
        name="budget", decimal_places=2, max_digits=20, default=0
    )
    slug = models.SlugField(blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = f"{slugify(self.name)}-{self.random_ascii()}"
        super().save(*args, **kwargs)

    def random_ascii(self) -> str:
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choice(chars) for _ in range(4))

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(end_date__gt=F("start_date")),
                name="end_date_greater_than_start_date",
            ),
        ]

    @property
    def is_active(self) -> bool:
        return date.today() < self.end_date

    @property
    def total_expenses(self) -> int:
        return self.expense_set.aggregate(Sum("amount"))["amount__sum"]

    @property
    def last_token(self) -> Optional[Token]:
        return (
            self.triptoken_set.order_by("expiry").last()
            if self.triptoken_set.count() > 0
            else None
        )


class Expense(models.Model):
    CATEGORY_CHOICES = [
        (Category.TRANSPORT.value, "Transport"),
        (Category.GROCERY.value, "Grocery"),
        (Category.ACTIVITY.value, "Activity"),
        (Category.RESTAURANT.value, "Restaurant"),
        (Category.ADMINISTRATIVE.value, "Administrative"),
    ]
    id: UUID = models.UUIDField(primary_key=True, default=uuid4)
    amount: float = models.DecimalField(name="amount", decimal_places=2, max_digits=20)
    label: str = models.CharField(name="label", max_length=255, default="")
    expense_date: date = models.DateField(name="expense_date")
    trip: Trip = models.ForeignKey(Trip, on_delete=models.CASCADE, default=None)
    category = models.CharField(
        max_length=len(max([category.value for category in Category], key=len)),
        choices=CATEGORY_CHOICES,
        null=True,
        blank=True,
    )


class TripToken(models.Model):
    token: str = models.CharField(max_length=255)
    expiry: str = models.DateTimeField()
    trip: Trip = models.ForeignKey(Trip, on_delete=models.CASCADE)


class Membership(models.Model):
    id: UUID = models.UUIDField(primary_key=True, default=uuid4)
    trip: Trip = models.ForeignKey(Trip, on_delete=models.CASCADE, default=None)
    user: User = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    membership_date: date = models.DateField(
        name="membership_date", default=timezone.now
    )
    can_create_expense: bool = models.BooleanField(
        name="can_create_expense", default=False
    )
    can_edit_expense: bool = models.BooleanField(name="can_edit_expense", default=False)
    can_delete_expense: bool = models.BooleanField(
        name="can_delete_expense", default=False
    )
    can_edit_trip: bool = models.BooleanField(name="can_edit_trip", default=False)
    can_share_trip: bool = models.BooleanField(name="can_share_trip", default=False)
    can_delete_trip: bool = models.BooleanField(name="can_delete_trip", default=False)
