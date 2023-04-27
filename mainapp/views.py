from typing import Any, Dict
from django.views.generic import TemplateView
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpRequest

from mainapp.models import Product, Cart, Order
from authapp.models import Profile


class ProductView(TemplateView):
    template_name: str = "mainapp/products.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(ProductView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        if not self.request.session.get('has_session'):
            self.request.session['has_session'] = True
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseRedirect:
        session_id = request.session.session_key
        profile_exists = Profile.objects.filter(Q(
            session_id=session_id) | Q(user__username=request.user)).exists()
        if request.user.is_authenticated:
            if not profile_exists:
                profile = Profile.create_profile(user=request.user)
                profile.save()
                cart = Cart.objects.create(profile=profile)
                cart.save()
        else:
            if not profile_exists:
                profile = Profile.create_profile(session_id=session_id)
                profile.save()
                cart = Cart.objects.create(profile=profile)
                cart.save()
        profile = Profile.objects.filter(
            Q(user__username=request.user) | Q(session_id=session_id)).first()
        cart = Cart.objects.filter(profile=profile).first()
        cart.add_product(product=request.POST.get('product_id'))
        return HttpResponseRedirect('/mainapp/')


class CartView(TemplateView):
    template_name = "mainapp/cart.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CartView, self).get_context_data(**kwargs)
        profile = Profile.objects.filter(
            Q(user__username=self.request.user) | Q(
                session_id=self.request.session.session_key)
        ).first()
        cart = Cart.objects.filter(
            profile=profile).first()
        context['profile'] = profile
        context['cart'] = cart
        context['total'] = cart.get_total_price()
        return context

    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponseRedirect:
        if request.POST.get('operation') == "order":
            profile = Profile.objects.filter(
                Q(user__username=self.request.user) | Q(
                    session_id=self.request.session.session_key)
            ).first()
            cart = Cart.objects.filter(
                profile=profile).first()
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            address = request.POST.get("address")
            phone = request.POST.get("phone")
            with transaction.atomic():
                profile.first_name = first_name
                profile.last_name = last_name
                profile.address = address
                profile.phone = phone
                profile.save()
                order = Order.objects.create(
                    profile=profile,
                    total_price=cart.get_total_price()
                )
                order.products.add(*cart.product.all())
                cart.clear()

        return HttpResponseRedirect('/mainapp/orders')


class OrdersView(TemplateView):
    template_name = "mainapp/orders.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(OrdersView, self).get_context_data(**kwargs)
        profile = Profile.objects.filter(
            Q(user__username=self.request.user) | Q(
                session_id=self.request.session.session_key)
        ).first()
        context['orders'] = Order.objects.filter(
            profile=profile
        )
        return context
