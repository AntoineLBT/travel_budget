from datetime import date
from decimal import Decimal

from bs4 import BeautifulSoup
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from hamcrest import assert_that, contains_string, is_

from accounting.constants import Category
from accounting.models import Expense
from accounting.tests.fixtures import AccountingFixtures
from www.tests import AuthenticatedClient


class ExpensePageTests(TestCase, AccountingFixtures):

    client_class = AuthenticatedClient

    def test_create_expense_page_login_required(self) -> None:
        """
        Given a unauthenticated client and trip
        When I get the create expense page
        Then it redirect to the login page
        """
        dummy_client = Client()

        page = dummy_client.get(
            reverse("create-expense", kwargs={"slug": self.any_trip().slug})
        )

        assert_that(page.status_code, is_(302))
        assert_that(page.url, contains_string("login"))

    def test_get_create_expense_page(self) -> None:
        """
        Given a client and a trip
        When I get the create expense page
        Then it return a 200 status
        """

        page = self.client.get(
            reverse("create-expense", kwargs={"slug": self.any_trip().slug})
        )

        assert_that(page.status_code, is_(200))

    def test_create_valid_expense(self) -> None:
        """
        Given a client and valid data to create an expense
        When I post on the create expense page
        Then it return a the trip consult page and the expense has been created
        """

        assert_that(Expense.objects.count(), is_(0))

        expense_label = "Réparation voiture"
        trip = self.any_trip()
        page = self.client.post(
            reverse("create-expense", kwargs={"slug": trip.slug}),
            data={
                "amount": Decimal(500.23),
                "label": expense_label,
                "expense_date": "2024-03-25",
                "category": Category.TRANSPORT.value,
                "trip": trip,
            },
        )
        assert_that(
            page.url,
            is_(reverse_lazy("consult-trip", kwargs={"slug": trip.slug})),
        )
        assert_that(Expense.objects.count(), is_(1))
        result_expense = Expense.objects.first()
        assert result_expense
        assert_that(result_expense.label, is_(expense_label))
        assert_that(result_expense.trip, is_(trip))

    def test_create_expense_date_consistence(self) -> None:
        """
        Given a client and an expense date not within the trip
        When I post on the create expense page
        Then it return the same page with an error
        """

        assert_that(Expense.objects.count(), is_(0))

        expense_label = "Réparation voiture"
        trip = self.any_trip()
        trip.start_date = date(2024, 3, 23)
        trip.end_date = date(2024, 3, 31)
        trip.save()
        page = self.client.post(
            reverse("create-expense", kwargs={"slug": trip.slug}),
            data={
                "amount": Decimal(500.23),
                "label": expense_label,
                "expense_date": "2024-02-25",
                "category": Category.TRANSPORT.value,
                "trip": trip,
            },
        )
        assert_that(
            page.wsgi_request.path,
            is_(reverse("create-expense", kwargs={"slug": trip.slug})),
        )
        assert_that(
            BeautifulSoup(page.content, "html.parser").select("[class~=alert]")[0].text,
            contains_string("Expense date"),
        )

    def test_edit_expense_initial(self) -> None:
        """
        Given a client and an expense
        When I get the edit expense page
        Then field are already filled
        """
        expense = self.any_expense()
        page = self.client.get(
            reverse(
                "edit-expense", kwargs={"slug": expense.trip.slug, "uuid": expense.id}
            )
        )
        soup = BeautifulSoup(page.content, "html.parser")
        assert_that(
            float(
                soup.find("form").find("input", attrs={"name": "amount"}).attrs["value"]
            ),
            is_(float(expense.amount)),
        )
        assert_that(
            soup.find("form")
            .find("select", attrs={"name": "category"})
            .option.attrs["value"],
            is_(expense.category),
        )
        assert_that(
            soup.find("form").find("input", attrs={"name": "label"}).attrs["value"],
            is_(expense.label),
        )
