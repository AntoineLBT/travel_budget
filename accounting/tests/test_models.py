from datetime import date

from django.test import TestCase
from django.utils import timezone
from hamcrest import assert_that, contains_string, instance_of, is_

from ..models import Budget, Expense


class BudgetTests(TestCase):
    def test_budget_model(self) -> None:
        budget = Budget.objects.create()
        assert_that(budget, is_(instance_of(Budget)))

    def test_budget_default_name(self) -> None:
        budget = Budget.objects.create()
        assert_that(
            budget.name, contains_string(timezone.now().strftime("%m/%d/%Y"))
        )


class ExpenseTests(TestCase):
    def test_expense_model(self) -> None:
        budget = Budget.objects.create()
        expense = Expense.objects.create(
            amount=100, label="Test", date=date(2022, 12, 31), budget=budget
        )
        assert_that(expense, is_(instance_of(Expense)))
