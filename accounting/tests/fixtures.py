from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from secrets import token_urlsafe
from typing import Any, Dict, Optional

from accounts.tests.fixtures import UserFixtures

from ..constants import Category
from ..models import Expense, Trip, TripToken


class AccountingFixtures(UserFixtures):
    def any_trip(self) -> Trip:
        user = self.any_user()
        trip = Trip.objects.create(
            owner=user,
            name="World Tour",
            description="My first world tour in 80 days",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
            budget=Decimal(10000),
        )
        trip.members.add(user)
        return trip

    def any_expense(self, kwargs: Optional[Dict[str, Any]] = {}) -> Expense:
        trip = kwargs.get("trip") or self.any_trip()
        user = kwargs.get("user") or trip.owner
        amount = kwargs.get("amount") or Decimal(3000)
        return Expense.objects.create(
            label="achat voiture",
            amount=amount,
            category=Category.TRANSPORT.value,
            expense_date=trip.start_date,
            trip=trip,
            user=user,
        )

    def any_trip_token(self, trip: Trip) -> TripToken:
        return TripToken.objects.create(
            token=token_urlsafe(32),
            expiry=datetime.now(tz=timezone.utc) + timedelta(days=1),
            trip=trip,
        )

    # def any_membership(
    #     self, trip: Optional[Trip] = None, user: Optional[User] = None
    # ) -> Membership:
    #     user = user or self.any_user()
    #     trip = trip or self.any_trip()
    #     return Membership.objects.create(trip=trip, user=user)
