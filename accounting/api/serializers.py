from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ..models import Expense, Trip


class ExpenseSerializer(ModelSerializer):

    class Meta:
        model = Expense
        fields = [
            "id",
            "amount",
            "label",
            "expense_date",
            "trip",
            "category",
            "user",
        ]


class TripSerializer(ModelSerializer):

    expense_set = SerializerMethodField()

    class Meta:
        model = Trip
        fields = [
            "id",
            "name",
            "description",
            "start_date",
            "end_date",
            "owner",
            "members",
            "slug",
            "expense_set",
        ]

    def get_expense_set(self, instance: Trip):

        queryset = instance.expense_set.filter(amount__gte=100)

        return ExpenseSerializer(queryset, many=True).data
