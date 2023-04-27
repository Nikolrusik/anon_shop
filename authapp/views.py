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

    def form_valid(self, form):
        response = super().form_valid(form)
        session_id = self.request.session.session_key
        profile, created = models.Profile.objects.get_or_create(
            session_id=session_id)
        profile.user = form.instance
        profile.save()
        return response


class CustomLoginView(LoginView):
    template_name: str = "authapp/login.html"
