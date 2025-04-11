from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from typing import Any

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.db.models.query import QuerySet
from django.forms import Form
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView, ListView, TemplateView

from accounting.models import Expense, Membership, Trip, TripToken
from accounts.models import User
from www.mixins import CustomPermissionRequiredMixin
from www.utility import get_trips_expenses_data, handle_permission

from .forms import (make_delete_expense_form, make_delete_member_form,
                    make_delete_trip_form, make_edit_member_form,
                    make_edit_profile_form, make_expense_form,
                    make_join_trip_form, make_login_form,
                    make_registration_form, make_trip_form)


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name: str = "dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["trips"] = Trip.objects.filter(members=self.request.user).order_by(
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


class EditProfileView(LoginRequiredMixin, FormView):
    template_name: str = "edit_profile.html"

    def get_form_class(self) -> type:
        return make_edit_profile_form(self.request)

    def get_success_url(self) -> str:
        return reverse("profile")

    def form_valid(self, form: Any) -> HttpResponse:

        User.objects.filter(email=form.cleaned_data["email"]).update(
            country=form.cleaned_data["country"],
            date_of_birth=form.cleaned_data["date_of_birth"],
            currency=form.cleaned_data["currency"],
        )

        return super().form_valid(form)


class CreateTripView(LoginRequiredMixin, FormView):
    template_name: str = "create_trip.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if "edit" in self.request.path:
            slug = self.request.path.split("/")[2]
            trip = Trip.objects.filter(members=self.request.user, slug=slug).first()
            handle_permission(
                trip=trip, user=self.request.user, permission="can_edit_trip"
            )

        return super().get(request, *args, **kwargs)

    def get_form_class(self):
        if "edit" in self.request.path:
            slug = self.request.path.split("/")[2]
            trip = Trip.objects.get(slug=slug)
        else:
            trip = None
        return make_trip_form(trip=trip)

    def form_valid(self, form):
        trip, created = Trip.objects.update_or_create(
            id=form.cleaned_data["id"],
            defaults={
                "name": form.cleaned_data["name"],
                "description": form.cleaned_data["description"],
                "start_date": form.cleaned_data["start_date"],
                "end_date": form.cleaned_data["end_date"],
                "budget": form.cleaned_data["budget"],
                "owner": self.request.user,
            },
        )

        if created:
            trip.members.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return (
            reverse("consult-trip", kwargs={"slug": self.request.path.split("/")[2]})
            if "edit" in self.request.path
            else reverse("dashboard")
        )


class JoinTripView(LoginRequiredMixin, FormView):
    template_name: str = "join_trip.html"
    trip = None

    def get_form_class(self):
        return make_join_trip_form()

    def form_valid(self, form: Any) -> HttpResponse:
        token = form.cleaned_data["token"]
        trip = TripToken.objects.get(token=token).trip
        trip.members.add(self.request.user.id)
        self.trip = trip
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("consult-trip", kwargs={"slug": self.trip.slug})


class ShareTripView(LoginRequiredMixin, CustomPermissionRequiredMixin, TemplateView):
    template_name: str = "share_trip.html"
    permissions = "can_share_trip"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        slug = self.request.path.split("/")[2]
        context["trip"] = Trip.objects.filter(
            members=self.request.user, slug=slug
        ).first()
        return context


class HTMXGenerateTokenView(
    LoginRequiredMixin, CustomPermissionRequiredMixin, TemplateView
):
    template_name: str = "htmx/generate_token.html"
    permissions = "can_share_trip"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        slug = self.request.path.split("/")[2]
        context = super().get_context_data(**kwargs)
        trip: Trip = Trip.objects.filter(members=self.request.user, slug=slug).first()
        context["trip"] = trip
        return context

    def put(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        slug = self.request.path.split("/")[2]
        trip: Trip = Trip.objects.filter(members=self.request.user, slug=slug).first()
        TripToken.objects.create(
            token=token_urlsafe(32),
            expiry=datetime.now(tz=timezone.utc) + timedelta(days=1),
            trip=trip,
        )
        return render(
            request=request,
            context=self.get_context_data(),
            template_name=self.template_name,
        )


class DeleteTripView(LoginRequiredMixin, CustomPermissionRequiredMixin, FormView):

    permissions = "can_delete_trip"

    def get_form_class(self):
        return make_delete_trip_form()

    def form_valid(self, form):
        Trip.objects.get(slug=self.request.POST["submit"]).delete()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("dashboard")


class TripView(LoginRequiredMixin, ListView):
    template_name: str = "trip.html"
    paginate_by = 20

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        slug = self.request.path.split("/")[2]
        context = super().get_context_data(**kwargs)
        context["trips"] = Trip.objects.filter(members=self.request.user, slug=slug)
        context["trip"] = context["trips"].first()
        context["budget_completion"] = (
            (context["trip"].total_expenses * 100) / context["trip"].budget
            if context["trip"].total_expenses
            else 0
        )
        context = get_trips_expenses_data(context=context)
        context["memberships"] = Membership.objects.filter(trip=context["trip"])
        return context

    def get_queryset(self) -> QuerySet[Any]:
        slug = slug = self.request.path.split("/")[2]
        order_by = self.request.GET.get("o")
        query = Trip.objects.get(slug=slug, members=self.request.user).expense_set.all()

        if order_by:
            for column in order_by.split("."):
                query = query.order_by(column)
        else:
            query = query.order_by("-expense_date")

        return query


class ExpenseView(LoginRequiredMixin, FormView):
    template_name: str = "create_expense.html"
    trip = None

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        trip_slug = self.request.path.split("/")[2]
        self.trip = Trip.objects.get(slug=trip_slug)
        if "edit_expense" in self.request.path:
            handle_permission(
                trip=self.trip,
                user=self.request.user,
                permission="can_edit_expense",
            )
        else:
            handle_permission(
                trip=self.trip, user=self.request.user, permission="can_create_expense"
            )
        return super().get(request, *args, **kwargs)

    def get_form_class(self) -> type:
        if "edit_expense" in self.request.path:
            expense_id = self.request.path.split("/")[4]
            expense = Expense.objects.get(id=expense_id)
        else:
            expense = None
        trip_slug = self.request.path.split("/")[2]
        return make_expense_form(
            trip=self.trip or Trip.objects.get(slug=trip_slug), expense=expense
        )

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
                "user": self.request.user,
            },
        )
        return super().form_valid(form)


class DeleteExpenseView(LoginRequiredMixin, CustomPermissionRequiredMixin, FormView):

    permissions = "can_delete_expense"

    def get_form_class(self):
        return make_delete_expense_form()

    def form_valid(self, form):
        Expense.objects.get(id=self.request.POST["id"]).delete()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        slug = self.request.path.split("/")[2]
        return reverse("consult-trip", kwargs={"slug": slug})


class DeleteMemberView(LoginRequiredMixin, CustomPermissionRequiredMixin, FormView):

    permissions = "can_delete_member"

    def get_form_class(self):
        return make_delete_member_form()

    def form_valid(self, form):
        membership = Membership.objects.get(id=self.request.POST["id"])
        trip = membership.trip
        trip.members.remove(membership.user)
        trip.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        slug = self.request.path.split("/")[2]
        return reverse("consult-trip", kwargs={"slug": slug})


class EditMemberView(LoginRequiredMixin, FormView):
    template_name = "edit_member.html"

    def get_form_class(self):
        trip = Trip.objects.get(slug=self.request.path.split("/")[2])
        membership_uuid = self.request.path.split("/")[-1]
        self.membership = Membership.objects.get(id=membership_uuid)
        return make_edit_member_form(trip, self.membership)

    def get_success_url(self):
        trip_slug = self.request.path.split("/")[2]
        return reverse("consult-trip", kwargs={"slug": trip_slug})

    def form_valid(self, form: Form):
        membership = Membership.objects.get(id=form.cleaned_data["id"])
        membership.can_create_expense = form.cleaned_data["can_create_expense"]
        membership.can_edit_expense = form.cleaned_data["can_edit_expense"]
        membership.can_delete_expense = form.cleaned_data["can_delete_expense"]
        membership.can_edit_trip = form.cleaned_data["can_edit_trip"]
        membership.can_share_trip = form.cleaned_data["can_share_trip"]
        membership.can_delete_trip = form.cleaned_data["can_delete_trip"]
        membership.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["membership"] = self.membership
        return context
