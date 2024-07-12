from accounting.models import Trip
from www.utility import handle_permission


class CustomPermissionRequiredMixin:

    permissions = ""

    def dispatch(self, request, *args, **kwargs):
        slug = self.request.path.split("/")[2]
        trip = Trip.objects.get(slug=slug)
        handle_permission(trip=trip, user=request.user, permission=self.permissions)
        return super().dispatch(request, *args, **kwargs)
