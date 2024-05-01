from datetime import datetime, timezone

from bs4 import BeautifulSoup
from django.test import Client, TestCase
from django.urls import reverse
from hamcrest import assert_that, contains_string, greater_than, is_, less_than

from accounting.models import TripToken
from accounting.tests.fixtures import AccountingFixtures
from accounts.models import User
from www.tests import AuthenticatedClient


class ShareTestPage(TestCase, AccountingFixtures):

    client_class = AuthenticatedClient

    def test_share_trip_login_required(self) -> None:
        """
        Given a unauthenticated client
        When I get the share trip page
        Then it redirect to the login page
        """
        dummy_client = Client()
        page = dummy_client.get(
            reverse("share-trip", kwargs={"slug": self.any_trip().slug})
        )
        assert_that(page.status_code, is_(302))
        assert_that(page.url, contains_string("login"))

    def test_share_trip_page_does_not_contain_token(self) -> None:
        """
        Given a client with a trip
        When I get the share trip page the first time
        Then it return a html page containing no token
        """

        user = User.objects.get(id=self.client.session["_auth_user_id"])
        trip = self.any_trip()
        trip.owner = user
        trip.members.add(user)
        trip.save()

        page = self.client.get(reverse("share-trip", kwargs={"slug": trip.slug}))
        soup = BeautifulSoup(page.content, "html.parser")
        assert_that(soup.find("b", attrs={"id": "token_string"}), is_(None))
        assert_that(TripToken.objects.count(), is_(0))


class HTMXGenerateTokenTests(TestCase, AccountingFixtures):

    client_class = AuthenticatedClient

    def test_generate_token_login_required(self) -> None:
        """
        Given a unauthenticated client
        When I get the generate token page
        Then it redirect to the login page
        """
        dummy_client = Client()
        page = dummy_client.get(
            reverse("htmx-generate-token", kwargs={"slug": self.any_trip().slug})
        )
        assert_that(page.status_code, is_(302))
        assert_that(page.url, contains_string("login"))

    def test_generate_token_produce_token(self) -> None:
        """
        Given a client with a trip
        When I put on the generate token page
        Then it return a html page containing the token
        """

        user = User.objects.get(id=self.client.session["_auth_user_id"])
        trip = self.any_trip()
        trip.owner = user
        trip.members.add(user)
        trip.save()

        page = self.client.put(
            reverse("htmx-generate-token", kwargs={"slug": trip.slug})
        )

        soup = BeautifulSoup(page.content, "html.parser")
        token_from_html = soup.find("b").text
        assert_that(TripToken.objects.count(), is_(1))
        assert_that(TripToken.objects.first().token, is_(token_from_html))

    def test_genereated_token_expiry(self) -> None:
        """
        Given a client with a trip
        When I put on the generate token page
        Then it return a html page containing the token expiring in more than 23h
        """

        user = User.objects.get(id=self.client.session["_auth_user_id"])
        trip = self.any_trip()
        trip.owner = user
        trip.members.add(user)
        trip.save()

        self.client.put(reverse("htmx-generate-token", kwargs={"slug": trip.slug}))

        assert_that(TripToken.objects.count(), is_(1))
        delta = TripToken.objects.first().expiry - datetime.now(tz=timezone.utc)
        assert_that(delta.seconds / 60 / 60, less_than(24))
        assert_that(delta.seconds / 60 / 60, greater_than(23))
