from typing import Any, Dict

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
