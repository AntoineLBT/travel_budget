from datetime import date

from django.test import TestCase
from hamcrest import assert_that, instance_of, is_

from ..models import Budget, Expense


class BudgetTests(TestCase):
    def test_budget_model(self) -> None:
        budget = Budget.objects.create()
        assert_that(budget, is_(instance_of(Budget)))


class ExpenseTests(TestCase):
    def test_expense_model(self) -> None:
        budget = Budget.objects.create()
        expense = Expense.objects.create(
            amount=100, label="Test", date=date(2022, 12, 31), budget=budget
        )
        assert_that(expense, is_(instance_of(Expense)))
