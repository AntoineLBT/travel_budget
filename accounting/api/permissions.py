from rest_framework.permissions import BasePermission

from ..models import Trip


class IsTripMember(BasePermission):
    def has_permission(self, request, view):
        trip = Trip.objects.filter(slug=request.GET.get("trip_slug", None)).first()
        return (
            request.user
            and request.user.is_authenticated
            and trip
            and request.user in trip.members.all()
        )
