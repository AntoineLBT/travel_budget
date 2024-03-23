from datetime import date

from accounts.tests.fixtures import UserFixtures

from ..models import Trip


class TripFixtures(UserFixtures):
    def any_trip(self):
        return Trip.objects.create(
            owner=self.any_user(),
            name="World Tour",
            description="My first world tour in 80 days",
            start_date=date(2024, 1, 1),
            end_date=date(2024, 12, 31),
        )
