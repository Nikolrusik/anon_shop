from typing import Union, Type, Dict
from django.db import models
from django.shortcuts import get_object_or_404
from authapp.models import AbstractUserModel, Profile


class Product(models.Model):
    name: str = models.CharField(verbose_name="Name", max_length=255)
    description: str = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True
    )
    # amount: int = models
    price: float = models.FloatField(verbose_name="Price")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Cart(models.Model):
    profile: Union[Type[Profile], str] = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Profile",
        db_index=True
    )
    product: Union[Type[Product], str] = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Product")
    amount: int = models.PositiveIntegerField(default=1, verbose_name="Amount")

    @classmethod
    def add_product(cls, profile, product, amount):
        new_product = cls(profile=profile, product=product, amount=amount)
        new_product.save()
        return new_product

    @classmethod
    def get_total_price(cls, profile):
        items = cls.objects.filter(profile=profile)
        return sum([int(item.amount) * int(item.product.price) for item in items])

    @classmethod
    def clear(cls, profile):
        items = cls.objects.filter(profile=profile)
        for item in items:
            item.delete()

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart items"


class Order(models.Model):
    profile: Union[Type[Profile], str] = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Profile",
        db_index=True
    )
    date_ordered: str = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Order date"
    )
    total_price: float = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Total price"
    )


class OrderItems(models.Model):
    order: Union[Type[Order], str] = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Order"
    )
    product: Union[Type[Product], str] = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Product"
    )
    amount: int = models.PositiveIntegerField(
        default=1,
        verbose_name="Amount"
    )

    class Meta:
        verbose_name = "Order item"
        verbose_name_plural = "Order items"
