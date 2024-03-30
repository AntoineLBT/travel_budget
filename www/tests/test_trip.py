from django.test import Client, TestCase
from django.urls import reverse
from hamcrest import assert_that, contains_string, is_

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
        trip.save()

        page = self.client.get(
            reverse("consult-trip", kwargs={"slug": trip.slug}),
        )
        assert_that(page.status_code, is_(200))
