from datetime import date
from decimal import Decimal

from accounts.tests.fixtures import UserFixtures

from ..constants import Category
from ..models import Expense, Trip


class AccountingFixtures(UserFixtures):
    def any_trip(self):
        return Trip.objects.create(
            owner=self.any_user(),
            name="World Tour",
            description="My first world tour in 80 days",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
        )

    def any_expense(self):
        trip = self.any_trip()
        return Expense.objects.create(
            label="achat voiture",
            amount=Decimal(3000),
            category=Category.TRANSPORT.value,
            expense_date=trip.start_date,
            trip=trip,
        )
