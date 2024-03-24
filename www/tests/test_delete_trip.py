from bs4 import BeautifulSoup
from django.test import TestCase
from django.urls import reverse
from hamcrest import assert_that, contains_string, is_

from accounting.models import Trip
from accounting.tests.fixtures import TripFixtures
from www.tests import AuthenticatedClient


class DeleteTripPageTests(TestCase, TripFixtures):

    client_class = AuthenticatedClient

    def test_delete_trip(self) -> None:

        trip = self.any_trip()
        assert_that(Trip.objects.count(), is_(1))

        page = self.client.post(
            reverse("delete-trip", kwargs={"slug": trip.slug}),
            data={"submit": trip.slug},
            follow=True,
        )

        assert_that(page.wsgi_request.path, is_("/dashboard"))
        assert_that(Trip.objects.count(), is_(0))
