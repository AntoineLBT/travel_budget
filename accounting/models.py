from datetime import date
from uuid import UUID, uuid4

from django.db import models

from accounts.models import User


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
    owner: User = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, related_name="trip_owner"
    )
    members: User = models.ManyToManyField(User)


class Expense(models.Model):
    id: UUID = models.UUIDField(primary_key=True, default=uuid4)
    amount: float = models.FloatField(name="amount", default=0)
    label: str = models.CharField(name="label", max_length=255, default="")
    expense_date: date = models.DateField(name="date")
    trip: Trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, default=None
    )
