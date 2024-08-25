from django.test import TestCase
from django.urls import reverse
from hamcrest import assert_that, is_

from accounts.tests.fixtures import UserFixtures
from www.tests import AuthenticatedClient


class LogoutViewTests(TestCase, UserFixtures):

    client_class = AuthenticatedClient

    def test_logout_view(self) -> None:
        """
        Given a connected user
        When I get the logout view
        Then it return the login page and client is not authenticated
        """

        page = self.client.post(reverse("logout"), follow=True)

        assert_that(page.wsgi_request.path, is_("/login"))
        assert_that(page.wsgi_request.user.is_authenticated, is_(False))
