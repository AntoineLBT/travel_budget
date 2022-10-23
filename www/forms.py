from crispy_forms import helper
from crispy_forms.layout import Layout, Submit
from django import forms


def make_login_form():
    class LoginForm(forms.Form):
        email: str = forms.EmailField(max_length=255, required=True)
        password: str = forms.CharField(widget=forms.PasswordInput())

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = helper.FormHelper()
            self.helper.form_id = "login-form"
            self.helper.form_method = "post"
            self.helper.layout = Layout(
                "email",
                "password",
                Submit("Se connecter", "se connecter"),
            )

    return LoginForm
