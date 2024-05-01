import re
from datetime import date, datetime, timezone
from typing import Any, Dict, Optional

from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms import helper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.urls import reverse

from accounting.constants import Category
from accounting.models import Expense, Trip, TripToken
from accounts.constants import Country, Currency
from accounts.models import User

from .utility import readonlish_field


def make_login_form(request) -> forms.Form:
    class LoginForm(forms.Form):
        email: str = forms.EmailField(max_length=255, required=True)
        password: str = forms.CharField(widget=forms.PasswordInput(), required=True)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = helper.FormHelper()
            self.helper.form_id = "login-form"
            self.helper.form_method = "post"
            self.helper.layout = Layout(
                FloatingField("email"),
                FloatingField("password"),
                Div(
                    Submit("connect", "Connect"),
                    css_class="d-flex justify-content-center",
                ),
            )

        def clean(self) -> Dict[str, Any]:
            cleaned_data = super().clean()
            assert cleaned_data
            user = User.objects.filter(email=cleaned_data["email"])
            username = user.first().username if user else None
            authenticated_user = authenticate(
                request=request,
                username=username,
                password=cleaned_data["password"],
            )
            if authenticated_user is None:
                raise forms.ValidationError("Password or/and email doesn't match")
            return cleaned_data

    return LoginForm


def make_registration_form() -> forms.Form:
    class RegistrationForm(forms.Form):
        email: str = forms.EmailField(max_length=255, required=True)
        username: str = forms.CharField(max_length=255, required=False)
        password: str = forms.CharField(
            max_length=255, widget=forms.PasswordInput(), required=True
        )
        password_confirmation: str = forms.CharField(
            max_length=255, widget=forms.PasswordInput(), required=True
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = helper.FormHelper()
            self.helper.form_id = "registration-form"
            self.helper.form_method = "post"
            self.helper.layout = Layout(
                FloatingField("email"),
                FloatingField("username"),
                FloatingField("password"),
                FloatingField("password_confirmation"),
                Div(
                    Submit("registration", "Sign up", css_class="mt-2"),
                    css_class="d-flex justify-content-center",
                ),
            )

        def clean(self) -> Dict[str, Any]:
            cleaned_data = super().clean()
            assert cleaned_data

            # Password validation
            pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
            if not bool(re.match(pattern, cleaned_data["password"])):
                raise forms.ValidationError(
                    """Password requirements : minimum 8 characters,
                    1 lowercase, 1 uppercase, 1 digits"""
                )

            if cleaned_data["password"] != cleaned_data["password_confirmation"]:
                raise forms.ValidationError("Passwords doesn't match")

            if User.objects.filter(email=cleaned_data["email"]).exists():
                raise forms.ValidationError("Email unavailable")

            if not cleaned_data["username"]:
                cleaned_data["username"] = cleaned_data["email"].split("@")[0]

            return cleaned_data

    return RegistrationForm


def make_join_trip_form() -> forms.Form:
    class JoinTripForm(forms.Form):
        token: str = forms.CharField(max_length=255, required=True)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = helper.FormHelper()
            self.helper.form_id = "join-trip-form"
            self.helper.form_method = "post"
            self.helper.layout = Layout(
                Div(
                    Div(FloatingField("token"), css_class="col-11"),
                    Div(
                        HTML(
                            """
                            <i class="bi bi-info-square mt-2" \
                        data-bs-toggle="tooltip" \
                        data-bs-placement="right" \
                        data-bs-original-title="Don't have a trip token ? \
                        Ask to the trip owner to generate one and share it to you.">
                    </i>"""
                        ),
                        css_class="col-1 mt-3",
                    ),
                    css_class="row",
                ),
                Div(
                    Submit("create", "Join trip", css_class="me-2"),
                    HTML("<a class='btn btn-secondary' href='/dashboard'>Cancel</a>"),
                    css_class="d-flex justify-content-center",
                ),
            )

        def clean(self):
            if not TripToken.objects.filter(token=self.cleaned_data["token"]).exists():
                raise ValidationError("This token does not exists.")

            token = TripToken.objects.get(token=self.cleaned_data["token"])

            if token.expiry < datetime.now(tz=timezone.utc):
                raise ValidationError("This token has expired.")

    return JoinTripForm


def make_trip_form(trip: Optional[Trip] = None) -> forms.Form:
    class TripForm(forms.Form):
        name: str = forms.CharField(max_length=255, required=True)
        description: str = forms.CharField(
            max_length=1023, required=False, widget=forms.Textarea
        )
        start_date: str = forms.DateField(
            required=True, widget=forms.DateInput(attrs={"type": "date"})
        )
        end_date: str = forms.DateField(
            required=True, widget=forms.DateInput(attrs={"type": "date"})
        )
        budget = forms.DecimalField(required=True)

        def __init__(self, *args, **kwargs):

            submit_text = "Edit this trip" if trip else "Create this trip"
            cancel_url = (
                reverse("consult-trip", kwargs={"slug": trip.slug})
                if trip
                else reverse("dashboard")
            )
            self.trip = trip

            super().__init__(*args, **kwargs)
            self.helper = helper.FormHelper()
            self.helper.form_id = "trip-form"
            self.helper.form_method = "post"
            self.helper.layout = Layout(
                FloatingField("name"),
                "description",
                FloatingField("start_date"),
                FloatingField("end_date"),
                FloatingField("budget"),
                Div(
                    Submit("create", submit_text, css_class="me-2"),
                    HTML(f'<a class="btn btn-secondary" href={cancel_url}>Cancel</a>'),
                    css_class="d-flex justify-content-center",
                ),
            )
            if self.trip:
                self.fields["name"].initial = trip.name
                self.fields["description"].initial = trip.description
                self.fields["start_date"].initial = trip.start_date
                self.fields["end_date"].initial = trip.end_date
                self.fields["budget"].initial = trip.budget

        def clean(self):
            if self.cleaned_data["start_date"] >= self.cleaned_data["end_date"]:
                raise ValidationError("Starting date can't be after the ending date")

    return TripForm


def make_delete_trip_form() -> forms.Form:
    class DeleteTripForm(forms.ModelForm):
        class Meta:
            model = Trip
            fields = []

    return DeleteTripForm


def make_expense_form(trip: Trip, expense: Optional[Expense] = None) -> forms.Form:
    class ExpenseForm(forms.Form):

        amount = forms.DecimalField(
            required=True, initial=expense.amount if expense else None
        )
        label: str = forms.CharField(
            max_length=255,
            required=True,
        )
        expense_date: str = forms.DateField(
            required=True,
            widget=forms.DateInput(attrs={"type": "date"}),
            initial=date.today,
        )
        category: str = forms.ChoiceField(
            choices=[(cat.value, cat.name) for cat in Category]
        )

        def __init__(self, *args, **kwargs):

            submit_text = "Edit this expense" if expense else "Add this expense"

            super().__init__(*args, **kwargs)
            self.trip = trip
            self.expense = expense
            self.helper = helper.FormHelper()
            self.helper.form_id = "trip-form"
            self.helper.form_method = "post"
            self.helper.layout = Layout(
                FloatingField("amount"),
                FloatingField("label"),
                FloatingField("expense_date"),
                "category",
                Div(
                    Submit("Add", submit_text, css_class="me-2"),
                    HTML(
                        f"""<a class="btn btn-secondary" href="""
                        f"""{reverse('consult-trip', kwargs={"slug":trip.slug})}>"""
                        f"""Cancel</a>"""
                    ),
                    css_class="d-flex justify-content-center",
                ),
            )
            if expense:
                self.fields["amount"].initial = expense.amount
                self.fields["label"].initial = expense.label
                self.fields["expense_date"].initial = expense.expense_date
                self.fields["category"].initial = expense.category

        def clean(self):
            self.cleaned_data["trip"] = self.trip
            self.cleaned_data["id"] = self.expense.id if expense else None
            if (
                self.trip.end_date < self.cleaned_data["expense_date"]
                or self.cleaned_data["expense_date"] < self.trip.start_date
            ):
                raise ValidationError(
                    f"Expense date must be within the trip date :"
                    f" {self.trip.start_date} to {self.trip.end_date}"
                )
            return self.cleaned_data

    return ExpenseForm


def make_delete_expense_form() -> forms.Form:
    class DeleteExpenseForm(forms.ModelForm):
        class Meta:
            model = Trip
            fields = []

    return DeleteExpenseForm


def make_edit_profile_form(request) -> forms.Form:
    class EditProfileForm(forms.Form):

        email = forms.CharField(max_length=255, required=True)
        username = forms.CharField(max_length=255, required=True)
        date_of_birth = forms.DateField(
            required=False,
            widget=forms.DateInput(attrs={"type": "date"}),
        )
        country = forms.ChoiceField(
            choices=[(cat.value, cat.name) for cat in Country], required=False
        )
        currency = forms.ChoiceField(
            choices=[(cat.value, cat.name) for cat in Currency], required=False
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.request = request
            self.helper = helper.FormHelper()
            self.helper.form_id = "trip-form"
            self.helper.form_method = "post"
            self.helper.layout = Layout(
                FloatingField("email"),
                FloatingField("username"),
                FloatingField("date_of_birth"),
                FloatingField("country"),
                FloatingField("currency"),
                Div(
                    Submit("update", "Update profile", css_class="me-2"),
                    HTML(
                        f"""<a class="btn btn-secondary" href="""
                        f"""{reverse('profile')}>"""
                        f"""Cancel</a>"""
                    ),
                    css_class="d-flex justify-content-center",
                ),
            )

            self.fields["email"].initial = self.request.user.email
            self.fields["username"].initial = self.request.user.username
            self.fields["date_of_birth"].initial = (
                self.request.user.date_of_birth
                if self.request.user.date_of_birth
                else date.today
            )
            self.fields["country"].initial = (
                self.request.user.country
                if self.request.user.country
                else Country.FRANCE.value
            )
            self.fields["currency"].initial = (
                self.request.user.currency
                if self.request.user.currency
                else Currency.EURO.value
            )
            readonlish_field(self.fields["email"])
            readonlish_field(self.fields["username"])

    return EditProfileForm
