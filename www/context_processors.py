from dataclasses import dataclass, field
from typing import List

from django.urls import reverse


@dataclass
class Action:
    link: str
    name: str
    icon: str


@dataclass
class Section:
    actions: List[Action] = field(default_factory=list)


def sidebar(request):
    main_section = Section()

    dashboard = Action(
        link=reverse("dashboard"), name="Dashboard", icon="fa-tachometer-alt"
    )
    profile = Action(link=reverse("profile"), name="Profile", icon="fa-user")

    main_section.actions.append(dashboard)
    main_section.actions.append(profile)

    return {"sidebar": [main_section]}
