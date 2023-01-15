from typing import Any, Dict

from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from accounts.models import User

from .forms import make_login_form, make_registration_form


class DashboardView(TemplateView):
    template_name: str = "dashboard.html"


class LoginView(FormView):
    template_name: str = "login.html"

    def get_form_class(self):
        return make_login_form()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = make_login_form()
        return context

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
        else:
            form.add_error(
                "password",
                error=ValidationError("Email or Password are wrong, please try again."),
            )
            return super().form_invalid(form)

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
