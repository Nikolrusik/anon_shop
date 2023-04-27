from django.contrib import admin
from mainapp.models import Product, Cart, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "price"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "profile", 'display_products']

    def display_products(self, obj):
        return ', '.join([product.name for product in obj.product.all()])
    display_products.short_description = 'Products'
