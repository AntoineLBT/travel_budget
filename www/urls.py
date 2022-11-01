from django.urls import path

from .views import HomeView, LoginView, RegistrationView

urlpatterns = [
    path("home", HomeView.as_view(), name="home"),
    path("login", LoginView.as_view(), name="login"),
    path("registration", RegistrationView.as_view(), name="registration"),
]
