from django.core.exceptions import PermissionDenied
from django.db.models import Sum

from accounting.constants import Category
from accounting.models import Membership, Trip
from accounts.models import User

BACKGROUND_COLOR = [
    "#fd7c7c",
    "#fdfd7c",
    "#7cfd7c",
    "#fc7cfd",
    "#fdee7c",
    "#ee7cfd",
    "#f6fd7c",
    "#7cfd83",
    "#7cf6fd",
    "#80fd7c",
    "#7cfdf9",
    "#7c80fd",
    "#7cfafd",
    "#7f7cfd",
    "#fd7cfa",
    "#7c7dfd",
    "#fd7c8b",
    "#fd7cd7",
]

HOVER_BACKGROUND_COLOR = [
    "#fdbd7c",
    "#bdfd7c",
    "#7cfdbd",
    "#b6fd7c",
    "#7cfdc3",
    "#7cb6fd",
    "#7cfdb9",
    "#7cc1fd",
    "#b97cfd",
    "#7cbafd",
    "#c07cfd",
    "#fd7cba",
    "#bb7cfd",
    "#fd7cbe",
    "#fdbb7c",
    "#fd7ccc",
    "#fdae7c",
    "#ccfd7c",
]


def get_trips_expenses_data(context: dict):

    total_amount_per_category = {cat.value: 0 for cat in Category}

    for trip in context["trips"]:
        sum_by_category = trip.expense_set.values("category").annotate(
            sum=Sum("amount")
        )
        for category in sum_by_category:
            total_amount_per_category[category["category"]] += float(category["sum"])

    context["labels"] = list(total_amount_per_category.keys())
    context["data"] = list(total_amount_per_category.values())
    context["background_color"] = BACKGROUND_COLOR[: len(context["labels"])]
    context["hover_background_color"] = HOVER_BACKGROUND_COLOR[: len(context["labels"])]
    return context


def readonlish_field(field):

    field.widget.attrs[
        "style"
    ] = """
                background-color: var(--bs-secondary-bg);
                opacity: 1;
                pointer-events:none;"""
    return field


def handle_permission(trip: Trip, user: User, permission: str):
    if not getattr(
        Membership.objects.filter(trip=trip, user=user).first(), permission, False
    ) and not (trip.owner.id is user.id):
        raise PermissionDenied
