from datetime import date

from django.urls import reverse_lazy
from hamcrest import assert_that, is_
from rest_framework.test import APITestCase

from accounting.tests.fixtures import AccountingFixtures


class TestTrip(APITestCase, AccountingFixtures):

    url = reverse_lazy("trip-list")

    def test_get_list(self):

        _, token = self.any_authenticated_user(self.client)

        self.any_trip()

        response = self.client.get(
            self.url, headers={"Authorization": f"Bearer {token}"}
        )

        assert_that(response.status_code, is_(200))

    def test_create_trip(self):

        user, token = self.any_authenticated_user(self.client)

        data = {
            "owner": user.pk,
            "name": "World Tour",
            "description": "My first world tour in 80 days",
            "start_date": date(2024, 1, 1).isoformat(),
            "end_date": date(2024, 12, 31).isoformat(),
            "budget": 10000,
        }

        response = self.client.post(
            self.url, data=data, headers={"Authorization": f"Bearer {token}"}
        )

        assert_that(response.status_code, is_(201))


class TestExpense(APITestCase, AccountingFixtures):

    def test_get_expense(self):

        user, token = self.any_authenticated_user(self.client)
        trip = self.any_trip(user)
        expense = self.any_expense(kwargs={"trip": trip, "user": trip.owner})

        response = self.client.get(
            f'{reverse_lazy("expense-list")}?trip_slug={trip.slug}',
            headers={"Authorization": f"Bearer {token}"},
        )

        assert_that(response.status_code, is_(200))
        assert_that(response.json()["results"][0]["id"], is_(str(expense.id)))
