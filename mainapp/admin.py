from django.contrib import admin
from mainapp.models import Product, Cart, Order, OrderItems


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "price"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "profile", 'product', 'amount']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "profile", 'date_ordered', 'total_price']


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ["order", 'product', 'amount']
