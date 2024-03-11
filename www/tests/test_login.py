from django.test import TestCase
from django.urls import reverse
from hamcrest import assert_that, contains_string, is_

from accounts.tests.fixtures import UserFixtures


class LoginPageTests(TestCase, UserFixtures):
    def test_get_login_page(self) -> None:
        """
        Given a client
        When a get the login page
        Then it return a 200
        """
        page = self.client.get(reverse("login"))
        assert_that(page.status_code, is_(200))

    def test_login_success(self) -> None:
        """
        Given a user with a default password toto
        When I send the following data to the login page:
            {"email": user.email, "password": "toto"}
        Then it return the dashboard page
        """

        user = self.any_user()

        page = self.client.post(
            reverse("login"),
            data={"email": user.email, "password": "toto"},
            follow=True,
        )
        assert_that(page.wsgi_request.path, is_("/dashboard"))

    def test_login_fail(self) -> None:
        """
        Given a user
        When I send invalid data to the login page
        Then it return the same page with a error message
        """

        self.any_user()
        page = self.client.post(
            reverse("login"),
            data={
                "email": "pas_le_bon_email@mail.com",
                "password": "paslebonmdp",
            },
            follow=True,
        )

        assert_that(page.wsgi_request.path, is_("/login"))
        assert_that(
            str(page.content),
            contains_string("Password or/and email doesn&#x27;t match"),
        )
