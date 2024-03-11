from django.test import Client, TestCase
from django.urls import reverse
from hamcrest import assert_that, contains_string, is_

from accounting.models import Trip
from accounts.tests.fixtures import UserFixtures
from www.tests import AuthenticatedClient


class CreateTripPageTests(TestCase, UserFixtures):

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
            },
            follow=True,
        )

        assert_that(page.wsgi_request.path, is_("/dashboard"))
        assert_that(Trip.objects.count(), is_(1))
        result_trip = Trip.objects.first()
        assert result_trip
        assert_that(result_trip.name, is_(trip_name))
        assert_that(result_trip.owner.username, is_(page.wsgi_request.user.username))
