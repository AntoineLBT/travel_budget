from django.test import Client, TestCase
from hamcrest import assert_that, contains_string, is_

from accounts.tests.fixtures import UserFixtures
from www.tests import AuthenticatedClient


class DashboardTests(TestCase, UserFixtures):

    client_class = AuthenticatedClient

    def test_dashboard_page_login_required(self) -> None:
        """
        Given a unauthenticated client
        When I get the dashboard page
        Then it redirect to the login page
        """
        dummy_client = Client()
        page = dummy_client.get("/create_trip")
        assert_that(page.status_code, is_(302))
        assert_that(page.url, contains_string("login"))
