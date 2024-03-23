from dataclasses import dataclass, field
from typing import List

from django.urls import reverse


@dataclass
class Action:
    link: str
    name: str
    icon: str
    path: str


@dataclass
class Section:
    actions: List[Action] = field(default_factory=list)


def sidebar(request):
    main_section = Section()

    dashboard = Action(
        link=reverse("dashboard"), name="Dashboard", icon="bi-grid", path="/dashboard"
    )
    profile = Action(
        link=reverse("profile"), name="Profile", icon="bi-person", path="/profile"
    )

    main_section.actions.append(dashboard)
    main_section.actions.append(profile)

    return {"sidebar": [main_section]}
