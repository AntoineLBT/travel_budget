from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models import Expense, Trip
from .permissions import IsTripMember
from .serializers import ExpenseSerializer, TripSerializer


class TripViewset(ModelViewSet):

    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trip.objects.all()


class ExpenseViewset(ModelViewSet):

    serializer_class = ExpenseSerializer
    permission_classes = [IsTripMember]

    def get_queryset(self):

        trip_slug = self.request.GET.get("trip_slug")
        trip = Trip.objects.filter(slug=trip_slug).first()

        return Expense.objects.filter(trip=trip) if trip else []
