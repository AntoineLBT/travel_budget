from datetime import date

from django.test import Client, TestCase
from django.urls import reverse
from hamcrest import assert_that, contains_string, is_

from accounts.constants import Country, Currency
from accounts.models import User
from accounts.tests.fixtures import UserFixtures
from www.tests import AuthenticatedClient


class ProfileTests(TestCase, UserFixtures):

    client_class = AuthenticatedClient

    def test_profile_page_login_required(self) -> None:
        """
        Given a unauthenticated client
        When I get the profile page
        Then it redirect to the login page
        """
        dummy_client = Client()
        page = dummy_client.get("/profile")
        assert_that(page.status_code, is_(302))
        assert_that(page.url, contains_string("login"))

    def test_edit_profile_login_required(self) -> None:
        """
        Given a unauthenticated client
        When I get the profile page
        Then it redirect to the login page
        """
        dummy_client = Client()
        page = dummy_client.get("/edit_profile")
        assert_that(page.status_code, is_(302))
        assert_that(page.url, contains_string("login"))

    def test_edit_profile_form_update_user(self) -> None:
        """
        Given a client and valid user data
        When a submit the form
        Then it return the profile page and the user has been updated
        """

        user = User.objects.get(id=self.client.session["_auth_user_id"])
        dob = date(1996, 7, 4)

        page = self.client.post(
            reverse("edit-profile"),
            data={
                "email": user.email,
                "username": user.username,
                "country": Country.FRANCE.value,
                "date_of_birth": dob,
                "currency": Currency.EURO.value,
            },
            follow=True,
        )

        user.refresh_from_db()

        assert_that(page.wsgi_request.path, is_("/profile"))
        assert_that(user.date_of_birth, is_(dob))
        assert_that(user.country, is_(Country.FRANCE.value))
        assert_that(user.currency, is_(Currency.EURO.value))
