from django.urls import path

from .views import (CreateTripView, CustomLogoutView, DashboardView,
                    DeleteExpenseView, DeleteMemberView, DeleteTripView,
                    EditProfileView, ExpenseView, HTMXGenerateTokenView,
                    JoinTripView, LoginView, ProfileView, RegistrationView,
                    ShareTripView, TripView)

urlpatterns = [
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", CustomLogoutView.as_view(), name="logout"),
    path("registration", RegistrationView.as_view(), name="registration"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("edit_profile", EditProfileView.as_view(), name="edit-profile"),
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
    path("trip/<slug:slug>/share", ShareTripView.as_view(), name="share-trip"),
    path(
        "trip/<slug:slug>/share/generate_token",
        HTMXGenerateTokenView.as_view(),
        name="htmx-generate-token",
    ),
    path("trip/<slug:slug>/edit", CreateTripView.as_view(), name="edit-trip"),
    path("join_trip", JoinTripView.as_view(), name="join-trip"),
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
    path(
        "trip/<slug:slug>/delete_member/<uuid:uuid>",
        DeleteMemberView.as_view(),
        name="delete-member",
    ),
    # path("trip/<slug:slug>/members", TripMembersView.as_view(), name="trip-members"),
]
