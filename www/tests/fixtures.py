from datetime import datetime

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
