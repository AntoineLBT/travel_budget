from typing import Any, Dict

from django.views.generic import FormView, TemplateView

from .forms import make_login_form


class HomeView(TemplateView):
    template_name: str = "home.html"


class LoginView(FormView):
    template_name: str = "login.html"

    def get_form_class(self):
        return make_login_form()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = make_login_form()
        return context
