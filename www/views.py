from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name: str = "home.html"


class LoginView(TemplateView):
    template_name: str = "login.html"


def index(request):
    return render(request, "dashboard/dashboard.html")
