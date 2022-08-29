from datetime import date

from django.test import TestCase

from ..models import Expense


# Create your tests here.
class ExpenseTests(TestCase):
    def test_representation(self) -> None:
        expense = Expense.objects.create(amount=100, label="Test", date=date(2022, 12, 31))
        assert isinstance(expense, Expense)
