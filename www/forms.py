from typing import Any, Dict

from crispy_forms import helper
from crispy_forms.layout import Layout, Submit
from django import forms

from accounts.models import User


def make_login_form() -> forms.Form:
    class LoginForm(forms.Form):
        email: str = forms.EmailField(max_length=255, required=True)
        password: str = forms.CharField(widget=forms.PasswordInput(), required=True)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = helper.FormHelper()
            self.helper.form_id = "login-form"
            self.helper.form_method = "post"
            # self.helper.form_class = "form-control"
            self.helper.layout = Layout(
                "email",
                "password",
                Submit("connect", "Connect", css_class="mt-2"),
            )

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
                "email",
                "username",
                "password",
                "password_confirmation",
                Submit("registration", "Create your account", css_class="mt-2"),
            )

        def clean(self) -> Dict[str, Any]:
            cleaned_data = super().clean()

            if cleaned_data["password"] != cleaned_data["password_confirmation"]:

                raise forms.ValidationError("Passwords doesn't match")

            if User.objects.filter(email=cleaned_data["email"]).exists():
                raise forms.ValidationError("Email unavailable")

            if not cleaned_data["username"]:
                cleaned_data["username"] = cleaned_data["email"].split("@")[0]

            return cleaned_data

    return RegistrationForm
