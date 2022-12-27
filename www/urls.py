from django.urls import path

from .views import DashboardView, LoginView, ProfileView, RegistrationView

urlpatterns = [
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("login", LoginView.as_view(), name="login"),
    path("registration", RegistrationView.as_view(), name="registration"),
    path("profile", ProfileView.as_view(), name="profile"),
]
