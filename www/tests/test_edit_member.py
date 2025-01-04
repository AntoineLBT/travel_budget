from bs4 import BeautifulSoup
from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from hamcrest import assert_that, contains_string, has_item, is_

from accounting.tests.fixtures import AccountingFixtures
from www.tests import AuthenticatedClient


class EditMemberPageTests(TestCase, AccountingFixtures):

    client_class = AuthenticatedClient

    def test_edit_membership__page_login_required(self) -> None:
        """
        Given a unauthenticated client and trip
        When I get the create expense page
        Then it redirect to the login page
        """
        dummy_client = Client()

        membership = self.any_membership()

        page = dummy_client.get(
            reverse(
                "edit-member",
                kwargs={"slug": membership.trip.slug, "uuid": membership.id},
            )
        )

        assert_that(page.status_code, is_(302))
        assert_that(page.url, contains_string("login"))

    def test_edit_membership__get_page(self) -> None:

        membership = self.any_membership()

        page = self.client.get(
            reverse(
                "edit-member",
                kwargs={"slug": membership.trip.slug, "uuid": membership.id},
            )
        )

        assert_that(page.status_code, is_(200))

    def test_edit_membership__post(self) -> None:
        """
        Given a membership without any permission
        When I get the edit membership page and select can_edit_trip
        Then the membership is accordingly updated
        """
        membership = self.any_membership()
        page = self.client.post(
            reverse(
                "edit-member",
                kwargs={"slug": membership.trip.slug, "uuid": membership.id},
            ),
            data={
                "can_create_expense": False,
                "can_edit_expense": False,
                "can_delete_expense": False,
                "can_edit_trip": True,
                "can_share_trip": False,
                "can_delete_trip": False,
            },
        )

        assert_that(
            page.url,
            is_(reverse_lazy("consult-trip", kwargs={"slug": membership.trip.slug})),
        )
        membership.refresh_from_db()

        assert_that(membership.can_edit_trip, is_(True))

    def test_edit_membership__initial_values(self) -> None:
        membership = self.any_membership()
        membership.can_create_expense = True
        membership.save()

        page = self.client.get(
            reverse(
                "edit-member",
                kwargs={"slug": membership.trip.slug, "uuid": membership.id},
            )
        )

        assert_that(page.status_code, is_(200))

        soup = BeautifulSoup(page.content, "html.parser")

        assert_that(
            soup.find("input", attrs={"name": "can_create_expense"}).attrs.keys(),
            has_item("checked"),
        )
