from uuid import UUID, uuid4
from django.db import models
from datetime import date
# Create your models here.
class Expense(models.Model):

    id: UUID = models.UUIDField(primary_key=True, default=uuid4)
    amount: float = models.FloatField(name="amount", default=0)
    label: str = models.CharField(name="label", max_length=255,default="")
    date: date = models.DateField(name="date")
