from typing import Any

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from accounting.models import Expense, Trip
from accounts.models import User
from www.utility import get_trips_expenses_data

from .forms import (make_delete_expense_form, make_delete_trip_form,
                    make_expense_form, make_login_form, make_registration_form,
                    make_trip_form)


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name: str = "dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["trips"] = Trip.objects.filter(owner=self.request.user).order_by(
            "-end_date"
        )
        context = get_trips_expenses_data(context=context)

        return context


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


class CustomLogoutView(LogoutView):
    def get_redirect_url(self) -> str:
        return reverse("login")


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


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name: str = "profile.html"


class CreateTripView(LoginRequiredMixin, FormView):
    template_name: str = "create_trip.html"

    def get_form_class(self):
        if "edit" in self.request.path:
            slug = self.request.path.split("/")[2]
            trip = Trip.objects.get(slug=slug)
        else:
            trip = None
        return make_trip_form(trip=trip)

    def form_valid(self, form):
        Trip.objects.create(
            name=form.cleaned_data["name"],
            description=form.cleaned_data["description"],
            start_date=form.cleaned_data["start_date"],
            end_date=form.cleaned_data["end_date"],
            budget=form.cleaned_data["budget"],
            owner=User.objects.get(email=self.request.user.email),
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("dashboard")


class DeleteTripView(LoginRequiredMixin, FormView):

    def get_form_class(self):
        return make_delete_trip_form()

    def form_valid(self, form):
        Trip.objects.get(slug=self.request.POST["submit"]).delete()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("dashboard")


class TripView(LoginRequiredMixin, TemplateView):
    template_name: str = "trip.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        slug = self.request.path.split("/")[2]
        context = super().get_context_data(**kwargs)
        context["trips"] = Trip.objects.filter(owner=self.request.user, slug=slug)
        context["trip"] = context["trips"].first()
        context["budget_completion"] = (
            (context["trip"].total_expenses * 100) / context["trip"].budget
            if context["trip"].total_expenses
            else 0
        )
        context = get_trips_expenses_data(context=context)
        return context


class ExpenseView(LoginRequiredMixin, FormView):
    template_name: str = "create_expense.html"

    def get_form_class(self) -> type:
        trip_slug = self.request.path.split("/")[2]
        if "edit_expense" in self.request.path:
            expense_id = self.request.path.split("/")[4]
            expense = Expense.objects.get(id=expense_id)
        else:
            expense = None
        return make_expense_form(trip=Trip.objects.get(slug=trip_slug), expense=expense)

    def get_success_url(self) -> str:
        trip_slug = self.request.path.split("/")[2]
        return reverse("consult-trip", kwargs={"slug": trip_slug})

    def form_valid(self, form):
        Expense.objects.update_or_create(
            id=form.cleaned_data["id"],
            defaults={
                "amount": form.cleaned_data["amount"],
                "label": form.cleaned_data["label"],
                "expense_date": form.cleaned_data["expense_date"],
                "trip": form.cleaned_data["trip"],
                "category": form.cleaned_data["category"],
            },
        )
        return super().form_valid(form)


class DeleteExpenseView(LoginRequiredMixin, FormView):

    def get_form_class(self):
        return make_delete_expense_form()

    def form_valid(self, form):
        Expense.objects.get(id=self.request.POST["id"]).delete()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        slug = self.request.path.split("/")[2]
        return reverse("consult-trip", kwargs={"slug": slug})
