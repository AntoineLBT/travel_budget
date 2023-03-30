from datetime import date
from uuid import UUID, uuid4

from django.db import models


class Budget(models.Model):
    id: UUID = models.UUIDField(primary_key=True, default=uuid4)
    name: str = models.CharField(
        name="name",
        max_length=255,
    )


class Expense(models.Model):
    id: UUID = models.UUIDField(primary_key=True, default=uuid4)
    amount: float = models.FloatField(name="amount", default=0)
    label: str = models.CharField(name="label", max_length=255, default="")
    expense_date: date = models.DateField(name="date")
    budget: Budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, default=None
    )
