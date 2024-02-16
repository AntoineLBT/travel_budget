from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from accounting.models import Trip
from accounts.models import User

from .forms import make_login_form, make_registration_form, make_trip_form


class DashboardView(TemplateView):
    template_name: str = "dashboard.html"


class LoginView(FormView):
    template_name: str = "login.html"

    def get_form_class(self):
        return make_login_form(self.request)

    def form_valid(self, form):
        email = self.request.POST["email"]
        user = User.objects.filter(email=email).first()
        username = user.username if user else None if email else None
        password = self.request.POST["password"]
        authenticated_user = authenticate(
            self.request, username=username, password=password
        )
        if authenticated_user:
            login(request=self.request, user=authenticated_user)
            return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("dashboard")


class RegistrationView(FormView):
    template_name: str = "registration.html"

    def get_form_class(self):
        return make_registration_form()

    def form_valid(self, form):
        User.objects.create_user(
            form.cleaned_data["username"],
            form.cleaned_data["email"],
            form.cleaned_data["password"],
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("login")


class ProfileView(TemplateView):
    template_name: str = "profile.html"


class CreateOrJoinTripView(TemplateView):
    template_name: str = "create_or_join_trip.html"


class CreateTripView(FormView):
    template_name: str = "create_trip.html"

    def get_form_class(self):
        return make_trip_form()

    def form_valid(self, form):
        Trip.objects.create(
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
            start_date=form.cleaned_data["start_date"],
            owner=User.objects.get(email=self.request.user.email),
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("dashboard")
