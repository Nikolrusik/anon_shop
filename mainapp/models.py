from typing import Union, Type
from django.db import models
from authapp.models import AbstractUserModel, Profile


class Product(models.Model):
    name: str = models.CharField(verbose_name="Name", max_length=255)
    description: str = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True
    )
    price: float = models.FloatField(verbose_name="Price")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Cart(models.Model):
    profile: Union[Type[Profile], str] = models.ForeignKey(
        AbstractUserModel,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Profile"
    )
    products: Union[Type[Product], str] = models.ManyToManyField(
        Product,
        verbose_name="Product"
    )

    def add_product(self, product):
        self.products.add(product)
        self.save()

    def get_total_price(self):
        return sum([product.price for product in self.products.all()])

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart items"


class Order(models.Model):
    profile: Union[Type[Profile], str] = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Profile"
    )
    date_ordered = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Order date"
    )
    products = models.ManyToManyField(
        Product,
        verbose_name="Products"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Total price"
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
