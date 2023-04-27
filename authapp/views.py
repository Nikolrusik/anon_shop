from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from authapp import models, forms


class RegiserView(CreateView):
    model: Any = get_user_model()
    form_class: Any = forms.RegisterForm
    success_url: str = reverse_lazy("mainapp:main")


class CustomLoginView(LoginView):
    template_name: str = "authapp/login.html"
