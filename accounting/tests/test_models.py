from datetime import date

from django.test import TestCase
from hamcrest import assert_that, instance_of, is_

from accounts.tests.fixtures import UserFixtures

from ..models import Expense, Trip


class TripTests(TestCase, UserFixtures):
    def test_trip_model(self) -> None:
        trip = Trip.objects.create(owner=self.any_user())
        assert_that(trip, is_(instance_of(Trip)))


class ExpenseTests(TestCase, UserFixtures):
    def test_expense_model(self) -> None:
        trip = Trip.objects.create(owner=self.any_user())
        expense = Expense.objects.create(
            amount=100, label="Test", date=date(2022, 12, 31), trip=trip
        )
        assert_that(expense, is_(instance_of(Expense)))
