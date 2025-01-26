from django import template
from django.http import QueryDict

from accounting.models import Membership, Trip
from accounts.models import User

register = template.Library()


@register.filter(name="any_data")
def any_data(data: list):
    return any(data)


@register.simple_tag(name="get_permission")
def get_permission(trip: Trip, user: User, permission: str):
    return (trip.owner.id is user.id) or getattr(
        Membership.objects.filter(trip=trip, user=user).first(), permission
    )


@register.simple_tag(name="is_owner")
def is_owner(trip_owner: User, membership_user: Membership):
    return trip_owner == membership_user


@register.simple_tag(name="get_url_order_by_name")
def get_url_order_by_name(query: QueryDict, column: str):
    order_query = query.get("o", "")

    if order_query:

        if f"-{column}" in order_query:
            order_query = column
        elif column in order_query:
            order_query = f"-{column}"
        else:
            order_query = column

        return order_query

    return column


@register.inclusion_tag("expense_column_order.html")
def expense_column_order(request, trip: Trip, column_name: str):
    return {"request": request, "trip": trip, "column_name": column_name}


# TODO : remove
# @register.filter(name="get_color")
# def get_color(colors: list, index: int):
#     return colors[index]

# @register.filter(name="disable_button")
# def disable_button():
#     return """style="background-color: var(--bs-secondary-bg);opacity: 1;
#             pointer-events:none;"""
