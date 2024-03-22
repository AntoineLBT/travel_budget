from django.urls import path

from .views import (CreateTripView, CustomLogoutView, DashboardView, LoginView,
                    ProfileView, RegistrationView)

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
]
