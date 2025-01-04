from django import template

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


# TODO : remove
# @register.filter(name="get_color")
# def get_color(colors: list, index: int):
#     return colors[index]

# @register.filter(name="disable_button")
# def disable_button():
#     return """style="background-color: var(--bs-secondary-bg);opacity: 1;
#             pointer-events:none;"""
