from django.test import TestCase
from django.urls import reverse
from hamcrest import assert_that, is_

from accounting.models import Trip
from accounting.tests.fixtures import AccountingFixtures
from accounts.models import User
from www.tests import AuthenticatedClient


class DeleteTripPageTests(TestCase, AccountingFixtures):

    client_class = AuthenticatedClient

    def test_delete_trip(self) -> None:

        user = User.objects.get(id=self.client.session["_auth_user_id"])
        trip = self.any_trip()
        trip.owner = user
        trip.save()
        assert_that(Trip.objects.count(), is_(1))

        page = self.client.post(
            reverse("delete-trip", kwargs={"slug": trip.slug}),
            data={"submit": trip.slug},
            follow=True,
        )

        assert_that(page.wsgi_request.path, is_("/dashboard"))
        assert_that(Trip.objects.count(), is_(0))

    def test_delete_trip_without_permission(self) -> None:
        """
        Given a user without permission on a given trip
        When I delete the trip
        Then it return a 403 status code
        """

        trip = self.any_trip()
        page = self.client.post(
            reverse("delete-trip", kwargs={"slug": trip.slug}),
            data={"submit": trip.slug},
            follow=True,
        )

        assert_that(page.status_code, is_(403))
