from django.urls import path
from mainapp import views
from django.contrib.auth.views import LogoutView
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", views.ProductView.as_view(), name="main"),
    # path("register/", views.RegiserView.as_view(), name="register"),
    # path("login/", views.CustomLoginView.as_view(), name="login"),
    # path("logout/", LogoutView.as_view(), name="logout"),
]
