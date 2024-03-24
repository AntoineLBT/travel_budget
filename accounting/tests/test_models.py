from datetime import date

from django.db.utils import IntegrityError
from django.test import TestCase
from hamcrest import assert_that, contains_string, instance_of, is_, none, not_

from ..models import Expense, Trip
from .fixtures import TripFixtures


class TripTests(TestCase, TripFixtures):
    def test_trip_model(self) -> None:
        trip = Trip.objects.create(
            owner=self.any_user(), start_date="2024-01-01", end_date="2024-12-31"
        )
        assert_that(trip, is_(instance_of(Trip)))

    def test_constraint_date(self) -> None:
        with self.assertRaises(IntegrityError) as exception:
            Trip.objects.create(
                owner=self.any_user(), start_date="2024-01-01", end_date="2023-12-31"
            )
        assert_that(
            exception.exception.args[0],
            contains_string("end_date_greater_than_start_date"),
        )

    def test_trip_slug(self) -> None:
        trip = self.any_trip()
        assert_that(trip.slug, is_(not_(none())))
        assert_that(trip.slug, contains_string("world-tour"))


class ExpenseTests(TestCase, TripFixtures):
    def test_expense_model(self) -> None:
        expense = Expense.objects.create(
            amount=100,
            label="Test",
            expense_date=date(2022, 12, 31),
            trip=self.any_trip(),
        )
        assert_that(expense, is_(instance_of(Expense)))
