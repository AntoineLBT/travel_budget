from datetime import datetime, timedelta, timezone

from bs4 import BeautifulSoup
from django.test import Client, TestCase
from django.urls import reverse
from hamcrest import assert_that, contains_string, is_

from accounting.models import Membership, Trip
from accounting.tests.fixtures import AccountingFixtures
from accounts.models import User
from www.tests import AuthenticatedClient


class JoinTripTestPage(TestCase, AccountingFixtures):

    client_class = AuthenticatedClient

    def test_join_trip_login_required(self) -> None:
        """
        Given a unauthenticated client
        When I get the join trip page
        Then it redirect to the login page
        """
        dummy_client = Client()
        page = dummy_client.get(reverse("join-trip"))
        assert_that(page.status_code, is_(302))
        assert_that(page.url, contains_string("login"))

    def test_join_trip_fake_token_display_error(self) -> None:
        """
        Given a client with a fake token
        When I post it on the join trip form
        Then it return the same page with an error
        """
        page = self.client.post(reverse("join-trip"), data={"token": "my_token"})

        assert_that(page.wsgi_request.path, is_(reverse("join-trip")))
        assert_that(
            BeautifulSoup(page.content, "html.parser").select("[class~=alert]")[0].text,
            contains_string("This token does not exists."),
        )

    def test_join_trip_add_members(self) -> None:
        """
        Given a client belonging to no trip
        When I post a valid trip's token
        Then it return the trip page on the client has been added as a member
        of the trip and a membership has been created
        """
        user = User.objects.get(id=self.client.session["_auth_user_id"])
        trip = self.any_trip()
        trip_token = self.any_trip_token(trip)

        assert_that(Trip.objects.filter(members=user).exists(), is_(False))

        page = self.client.post(
            reverse("join-trip"), data={"token": trip_token.token}, follow=True
        )

        assert_that(
            page.wsgi_request.path,
            is_(reverse("consult-trip", kwargs={"slug": trip.slug})),
        )
        assert_that(Trip.objects.filter(members=user).first(), is_(trip))
        assert_that(Membership.objects.filter(trip=trip, user=user).exists(), is_(True))

    def test_join_trip_expired_token(self) -> None:
        """
        Given a client belonging to no trip
        When I post an expired trip's token
        Then it return the same page with a error message
        """

        trip_token = self.any_trip_token(self.any_trip())
        trip_token.expiry = datetime.now(tz=timezone.utc) - timedelta(days=1)
        trip_token.save()

        page = self.client.post(reverse("join-trip"), data={"token": trip_token.token})
        assert_that(page.wsgi_request.path, is_(reverse("join-trip")))
        assert_that(
            BeautifulSoup(page.content, "html.parser").select("[class~=alert]")[0].text,
            contains_string("This token has expired."),
        )
