from datetime import date
from uuid import UUID, uuid4

from django.db import models
from django.db.models import Sum

from accounts.models import User

from .constants import Category


class Trip(models.Model):
    id: UUID = models.UUIDField(primary_key=True, default=uuid4)
    name: str = models.CharField(
        name="name",
        max_length=255,
    )
    description: str = models.TextField(
        name="description", max_length="1023", default=""
    )
    start_date: date = models.DateField(name="start_date", default=date.today)
    end_date: date = models.DateField(name="end_date", default=date.today)
    owner: User = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, related_name="trip_owner"
    )
    members: User = models.ManyToManyField(User)

    @property
    def is_active(self) -> bool:
        return date.today() < self.end_date

    @property
    def total_expenses(self) -> int:
        return self.expense_set.aggregate(Sum("amount"))["amount__sum"]


class Expense(models.Model):
    CATEGORY_CHOICES = [
        (Category.TRANSPORT.value, "Transport"),
        (Category.GROCERY.value, "Grocery"),
        (Category.ACTIVITY.value, "Activity"),
        (Category.RESTAURANT.value, "Restaurant"),
        (Category.ADMINISTRATIVE.value, "Administrative"),
    ]
    id: UUID = models.UUIDField(primary_key=True, default=uuid4)
    amount: float = models.FloatField(name="amount", default=0)
    label: str = models.CharField(name="label", max_length=255, default="")
    expense_date: date = models.DateField(name="date")
    trip: Trip = models.ForeignKey(Trip, on_delete=models.CASCADE, default=None)
    category = models.CharField(
        max_length=len(max([category.value for category in Category], key=len)),
        choices=CATEGORY_CHOICES,
        null=True,
        blank=True,
    )
