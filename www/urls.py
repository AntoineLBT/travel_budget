from django.urls import path

from .views import (CreateExpenseView, CreateTripView, CustomLogoutView,
                    DashboardView, LoginView, ProfileView, RegistrationView,
                    TripView)

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
    path("trip/<slug:slug>/consult", TripView.as_view(), name="trip-consult"),
    path(
        "trip/<slug:slug>/create_expense",
        CreateExpenseView.as_view(),
        name="trip-create-expense",
    ),
]
