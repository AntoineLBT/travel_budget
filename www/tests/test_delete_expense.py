from django.test import TestCase
from django.urls import reverse
from hamcrest import assert_that, is_

from accounting.models import Expense
from accounting.tests.fixtures import AccountingFixtures
from accounts.models import User
from www.tests import AuthenticatedClient


class DeleteExpensePageTests(TestCase, AccountingFixtures):

    client_class = AuthenticatedClient

    def test_delete_expense(self) -> None:

        expense = self.any_expense()
        expense.trip.owner = User.objects.get(id=self.client.session["_auth_user_id"])
        expense.trip.save()

        assert_that(Expense.objects.count(), is_(1))
        page = self.client.post(
            reverse(
                "delete-expense",
                kwargs={"slug": expense.trip.slug, "uuid": expense.id},
            ),
            data={"id": expense.id},
        )

        assert_that(
            page.url,
            is_(reverse("consult-trip", kwargs={"slug": expense.trip.slug})),
        )
        assert_that(Expense.objects.count(), is_(0))

    def test_delete_expense_without_permission(self) -> None:
        """
        Given a user member of a trip but without permission
        When I try to delete an expense
        Then it return a 403 status code
        """

        expense = self.any_expense()

        page = self.client.post(
            reverse(
                "delete-expense",
                kwargs={"slug": expense.trip.slug, "uuid": expense.id},
            ),
            data={"id": expense.id},
        )

        assert_that(page.status_code, is_(403))
