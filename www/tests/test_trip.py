from decimal import Decimal

from bs4 import BeautifulSoup
from django.test import Client, TestCase
from django.urls import reverse
from hamcrest import assert_that, contains_string, is_

from accounting.constants import Category
from accounting.models import Expense
from accounting.tests.fixtures import AccountingFixtures
from accounts.models import User
from www.tests import AuthenticatedClient


class TripPageTests(TestCase, AccountingFixtures):

    client_class = AuthenticatedClient

    def test_trip_page_login_required(self) -> None:
        """
        Given a unauthenticated client
        When I get the trip page
        Then it redirect to the login page
        """
        dummy_client = Client()
        page = dummy_client.get(
            reverse("consult-trip", kwargs={"slug": self.any_trip().slug})
        )
        assert_that(page.status_code, is_(302))
        assert_that(page.url, contains_string("login"))

    def test_get_trip_page(self) -> None:
        """
        Given a client
        When I get the consult trip page
        Then it return a 200 status
        """
        user = User.objects.get(id=self.client.session["_auth_user_id"])
        trip = self.any_trip()
        trip.owner = user
        trip.members.add(user)
        trip.save()

        page = self.client.get(
            reverse("consult-trip", kwargs={"slug": trip.slug}),
        )
        assert_that(page.status_code, is_(200))

    def test_pagination_number_of_expenses(self) -> None:
        """
        Given a client and a trip with 100 expenses
        When I get the trip page
        Then it return a table containing 20 expenses
        """

        user = User.objects.get(id=self.client.session["_auth_user_id"])
        trip = self.any_trip()
        trip.owner = user
        trip.members.add(user)
        trip.save()

        for i in range(1, 101):
            Expense.objects.create(
                amount=1 * Decimal(1),
                label=f"exp_{i}",
                expense_date="2024-04-01",
                category=Category.TRANSPORT.value,
                trip=trip,
            )

        page = self.client.get(reverse("consult-trip", kwargs={"slug": trip.slug}))

        soup = BeautifulSoup(page.content, "html.parser")
        assert_that(len(soup.find(id="expense_table").find_all("tr")), is_(21))

    def test_expense_pagination(self) -> None:
        """
        Given a client and a trip with 100 expenses
        When I get the second page of expense on the trip page
        Then it return a table containing expenses from 21 to 40
        """

        user = User.objects.get(id=self.client.session["_auth_user_id"])
        trip = self.any_trip()
        trip.owner = user
        trip.members.add(user)
        trip.save()

        for i in range(1, 101):
            Expense.objects.create(
                amount=Decimal(i),
                label=f"exp_{i}",
                expense_date="2024-04-01",
                category=Category.TRANSPORT.value,
                trip=trip,
            )

        page = self.client.get(
            f'{reverse("consult-trip", kwargs={"slug": trip.slug})}?page=2'
        )

        soup = BeautifulSoup(page.content, "html.parser")
        assert_that(
            soup.find(id="expense_table").find_all("tr")[1].find("td").text,
            contains_string("21"),
        )
        assert_that(
            soup.find(id="expense_table").find_all("tr")[-1].find("td").text,
            contains_string("40"),
        )
