from datetime import datetime
from typing import Tuple

from django.test import Client
from django.urls import reverse_lazy

from accounts.models import User


class UserFixtures:
    def any_user(self):
        username = f"toto_{datetime.now().microsecond}"
        user = User.objects.create(
            username=username, email=f"{username}@gmail.com", password="toto"
        )
        user.set_password("toto")
        user.save()
        return user

    def any_authenticated_user(self, client: Client) -> Tuple[User, str]:
        user = self.any_user()
        response = client.post(
            reverse_lazy("token-obtain-pair"),
            data={"username": user.username, "password": "toto"},
        )
        return user, response.json()["access"]
