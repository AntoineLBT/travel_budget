import random
import string
from datetime import date
from uuid import UUID, uuid4

from django.db import models
from django.db.models import CheckConstraint, F, Q, Sum
from django.template.defaultfilters import slugify

from accounts.models import User

from .constants import Category


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
    token: str = models.CharField(max_length=255, null=True, blank=True)
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
