from django.test import TestCase
from django.urls import reverse
from hamcrest import assert_that, contains_string, is_

from accounts.models import User

from .fixtures import UserFixtures


class RegistrationPageTests(TestCase, UserFixtures):
    def test_get_registration_page(self) -> None:
        """
        Given a client
        When I get the registration page
        Then it return a 200 status
        """
        page = self.client.get("/registration")

        assert_that(page.status_code, is_(200))

    def test_registration_success(self) -> None:
        """
        When I send the following data to the registration page :
            {
                "email": "toto@email.com",
                "username": "toto",
                "password": "toto1234",
                "password_confirmation": "toto1234"
            }
        Then it return the login page and a user has been created
        with the same data
        """

        assert_that(User.objects.count(), is_(0))

        page = self.client.post(
            reverse("registration"),
            data={
                "email": "toto@email.com",
                "username": "toto",
                "password": "toto1234",
                "password_confirmation": "toto1234",
            },
            follow=True,
        )

        assert_that(page.wsgi_request.path, is_("/login"))
        assert_that(User.objects.count(), is_(1))
        assert_that(User.objects.first().email, is_("toto@email.com"))

    def test_registration_same_email(self) -> None:
        """
        Given a registration form
        When I send the same email twice
        Then it return the same page with an error message
        and only 1 user exists
        """

        data = {
            "email": "toto@email.com",
            "username": "toto",
            "password": "toto1234",
            "password_confirmation": "toto1234",
        }

        assert_that(User.objects.count(), is_(0))

        self.client.post(
            reverse("registration"),
            data=data,
            follow=True,
        )

        page = self.client.post(
            reverse("registration"),
            data=data,
            follow=True,
        )

        assert_that(page.wsgi_request.path, is_("/registration"))
        assert_that(User.objects.count(), is_(1))
        assert_that(str(page.content), contains_string("Email unavailable"))

    def test_registration_different_password(self) -> None:
        """
        Given a registration form
        When I same two different password
        Then it return the same page with an error message
        and no user has been created
        """

        assert_that(User.objects.count(), is_(0))

        page = self.client.post(
            reverse("registration"),
            data={
                "email": "toto@email.com",
                "username": "toto",
                "password": "toto1234",
                "password_confirmation": "toto5678",
            },
            follow=True,
        )

        assert_that(page.wsgi_request.path, is_("/registration"))
        assert_that(User.objects.count(), is_(0))
        assert_that(
            str(page.content),
            contains_string("Passwords doesn&#x27;t match"),
        )