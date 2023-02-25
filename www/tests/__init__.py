from django.test import Client

from accounts.models import User


class AuthenticatedClient(Client):
    def __init__(self):
        super().__init__()
        user = User.objects.create(
            username="john",
            email="john.doe@gmail.com",
            password="onion",
        )
        self.force_login(user=user)
