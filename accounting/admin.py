from django.contrib import admin

from .models import Expense, Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "owner", "start_date", "end_date"]


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["amount", "label", "date", "category"]
