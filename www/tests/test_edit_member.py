from django.test import Client, TestCase
from django.urls import reverse, reverse_lazy
from hamcrest import assert_that, contains_string, is_

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

    def test_edit_membership(self) -> None:
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
