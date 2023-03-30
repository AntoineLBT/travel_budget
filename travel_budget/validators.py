import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class PasswordValidator(object):
    def validate(self, password, user=None):
        if not re.fullmatch(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",  # noqa: E501
            password,
        ):
            raise ValidationError(
                _(
                    """The password must contain at least :\n
                1 digit, 0-9\n
                1 uppercase, A-Z
                1 lowercase, a-z
                1 special caracter, @$!%*?&
                minimum 8 caracter"""
                ),
                code="password_no_number",
            )

    def get_help_text(self):
        return _(
            "Your password must contain Minimum eight characters, at least"
            "one uppercase letter, one lowercase letter, one number and one"
            "special character"
        )
