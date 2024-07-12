from decimal import Decimal

from bs4 import BeautifulSoup
from django.test import Client, TestCase
from django.urls import reverse
from hamcrest import assert_that, contains_string, is_

from accounting.models import Trip
from accounting.tests.fixtures import AccountingFixtures
from accounts.models import User
from www.tests import AuthenticatedClient


class CreateTripPageTests(TestCase, AccountingFixtures):

    client_class = AuthenticatedClient

    def test_create_trip_page_login_required(self) -> None:
        """
        Given a unauthenticated client
        When I get the create trip page
        Then it redirect to the login page
        """
        dummy_client = Client()
        page = dummy_client.get("/create_trip")
        assert_that(page.status_code, is_(302))
        assert_that(page.url, contains_string("login"))

    def test_get_create_trip_page(self) -> None:
        """
        Given a client
        When I get the create trip page
        Then it return a 200 status
        """
        page = self.client.get("/create_trip")

        assert_that(page.status_code, is_(200))

    def test_create_valid_trip(self) -> None:
        """
        Given a client and valid data to create a trip
        When I post on the create trip page
        Then it return a 201 status
        """

        assert_that(Trip.objects.count(), is_(0))

        trip_name = "Mon premier voyage"

        page = self.client.post(
            reverse("create-trip"),
            data={
                "name": trip_name,
                "description": "Mon premier voyage sur un autre continent",
                "start_date": "2024-02-25",
                "end_date": "2024-04-25",
                "budget": Decimal(1),
            },
            follow=True,
        )

        assert_that(page.wsgi_request.path, is_("/dashboard"))
        assert_that(Trip.objects.count(), is_(1))
        result_trip = Trip.objects.first()
        assert result_trip
        assert_that(result_trip.name, is_(trip_name))
        assert_that(result_trip.owner.username, is_(page.wsgi_request.user.username))

    def test_create_trip_date_consistence(self) -> None:
        """
        Given a client and invalid date order
        When I post on the create trip page
        Then it return the same page with an error
        """
        page = self.client.post(
            reverse("create-trip"),
            data={
                "name": "mon premier voyage",
                "description": "Mon premier voyage sur un autre continent",
                "start_date": "2024-02-25",
                "end_date": "2024-01-25",
                "budget": Decimal(1),
            },
            follow=True,
        )
        assert_that(page.wsgi_request.path, is_("/create_trip"))
        assert_that(
            BeautifulSoup(page.content, "html.parser").select("[class~=alert]")[0].text,
            contains_string("Starting date"),
        )

    def test_edit_trip_initial(self) -> None:
        """
        Given a client and a trip
        When I get the edit trip page
        Then field are already filled
        """

        user = User.objects.get(id=self.client.session["_auth_user_id"])
        trip = self.any_trip()
        trip.owner = user
        trip.members.add(user)
        trip.save()
        page = self.client.get(reverse("edit-trip", kwargs={"slug": trip.slug}))
        soup = BeautifulSoup(page.content, "html.parser")
        assert_that(
            soup.find("form").find("input", attrs={"name": "name"}).attrs["value"],
            is_(trip.name),
        )
        assert_that(
            soup.find("form")
            .find("textarea", attrs={"name": "description"})
            .contents[0],
            contains_string(trip.description),
        )
        assert_that(
            soup.find("form")
            .find("input", attrs={"name": "start_date"})
            .attrs["value"],
            is_(str(trip.start_date)),
        )
        assert_that(
            soup.find("form").find("input", attrs={"name": "end_date"}).attrs["value"],
            is_(str(trip.end_date)),
        )
        assert_that(
            float(
                soup.find("form").find("input", attrs={"name": "budget"}).attrs["value"]
            ),
            is_(float(trip.budget)),
        )
