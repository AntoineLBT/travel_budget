from django.urls import path

from .views import (CreateTripView, CustomLogoutView, DashboardView,
                    DeleteExpenseView, DeleteTripView, ExpenseView, LoginView,
                    ProfileView, RegistrationView, TripView)

urlpatterns = [
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", CustomLogoutView.as_view(), name="logout"),
    path("registration", RegistrationView.as_view(), name="registration"),
    path("profile", ProfileView.as_view(), name="profile"),
    path(
        "create_trip",
        CreateTripView.as_view(),
        name="create-trip",
    ),
    path(
        "trip/<slug:slug>/delete",
        DeleteTripView.as_view(),
        name="delete-trip",
    ),
    path("trip/<slug:slug>/consult", TripView.as_view(), name="consult-trip"),
    path("trip/<slug:slug>/edit", CreateTripView.as_view(), name="edit-trip"),
    path(
        "trip/<slug:slug>/create_expense",
        ExpenseView.as_view(),
        name="create-expense",
    ),
    path(
        "trip/<slug:slug>/edit_expense/<uuid:uuid>",
        ExpenseView.as_view(),
        name="edit-expense",
    ),
    path(
        "trip/<slug:slug>/delete_expense/<uuid:uuid>",
        DeleteExpenseView.as_view(),
        name="delete-expense",
    ),
]
