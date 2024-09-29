from datetime import date
from decimal import Decimal

from django.db.utils import IntegrityError
from django.test import TestCase
from hamcrest import assert_that, contains_string, instance_of, is_, none, not_

from ..models import Expense, Membership, Trip
from .fixtures import AccountingFixtures


class TripTests(TestCase, AccountingFixtures):
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

    def test_trip_is_active(self) -> None:
        trip = self.any_trip()
        trip.start_date = date(2023, 1, 1)
        trip.end_date = date(2023, 12, 25)
        trip.save()

        assert_that(trip.is_active, is_(False))


class ExpenseTests(TestCase, AccountingFixtures):
    def test_expense_model(self) -> None:

        trip = self.any_trip()

        expense = Expense.objects.create(
            amount=100,
            label="Test",
            expense_date=date(2022, 12, 31),
            trip=trip,
            user=trip.owner,
        )
        assert_that(expense, is_(instance_of(Expense)))


class MembershipTests(TestCase, AccountingFixtures):
    def test_membership_total_expenses(self) -> None:
        """
        Given a user in a trip with 2 expenses
        When I get the total_expenses of the member
        Then I get the sum of the 2 expenses
        """

        trip = self.any_trip()

        exp_1 = self.any_expense(
            {"trip": trip, "amount": Decimal(123), "user": trip.owner}
        )
        exp_2 = self.any_expense(
            {"trip": trip, "amount": Decimal(177), "user": trip.owner}
        )

        m = Membership.objects.get(trip=trip, user=trip.owner)

        assert_that(m.total_expenses, is_(exp_1.amount + exp_2.amount))
