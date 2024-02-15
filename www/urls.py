from django.urls import path

from .views import (CreateOrJoinTripView, DashboardView, LoginView,
                    ProfileView, RegistrationView)

urlpatterns = [
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("login", LoginView.as_view(), name="login"),
    path("registration", RegistrationView.as_view(), name="registration"),
    path("profile", ProfileView.as_view(), name="profile"),
    path(
        "create_or_join_trip",
        CreateOrJoinTripView.as_view(),
        name="create-or-join-trip",
    ),
]
