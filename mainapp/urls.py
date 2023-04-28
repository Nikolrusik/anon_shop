from django.urls import path
from mainapp import views
from django.contrib.auth.views import LogoutView
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", views.ProductView.as_view(), name="main"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("orders/", views.OrdersView.as_view(), name="orders"),
    path("order/<int:pk>", views.OrderListView.as_view(), name="order_list"),
]
