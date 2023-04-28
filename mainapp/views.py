from typing import Any, Dict
from django.views.generic import TemplateView
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpRequest

from mainapp.models import Product, Cart, Order, OrderItems
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
        session_id: str = request.session.session_key
        profile_exists: bool = Profile.objects.filter(Q(
            session_id=session_id) | Q(user__username=request.user)).exists()
        product = Product.objects.get(id=request.POST.get("product_id"))
        amount = request.POST.get("amount")
        if request.user.is_authenticated:
            if not profile_exists:
                profile: Union[Type[Profile], str] = Profile.create_profile(
                    user=request.user)
                profile.save()
        else:
            if not profile_exists:
                profile: Union[Type[Profile], str] = Profile.create_profile(
                    session_id=session_id)
                profile.save()
        profile: Union[Type[Profile], str] = Profile.objects.filter(
            Q(user__username=request.user) | Q(session_id=session_id)).first()
        cart: Any = Cart.objects.create(
            profile=profile,
            product=product,
            amount=amount
        )
        cart.save()
        return HttpResponseRedirect('/mainapp/')


class CartView(TemplateView):
    template_name = "mainapp/cart.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CartView, self).get_context_data(**kwargs)
        profile: Union[Type[Profile], str] = Profile.objects.filter(
            Q(user__username=self.request.user) | Q(
                session_id=self.request.session.session_key)
        ).first()
        cart: Union[Type[Cart], str] = Cart.objects.filter(
            profile=profile)
        context['profile'] = profile
        context['cart'] = cart
        context['total'] = Cart.get_total_price(profile)
        return context

    def post(self, request: HttpRequest, **kwargs: Dict[str, Any]) -> HttpResponseRedirect:
        if request.POST.get('operation') == "order":
            profile: Union[Type[Profile], str] = Profile.objects.filter(
                Q(user__username=self.request.user) | Q(
                    session_id=self.request.session.session_key)
            ).first()
            cart: Dict[Type[Cart], str] = Cart.objects.filter(
                profile=profile)
            first_name: str = request.POST.get("first_name")
            last_name: str = request.POST.get("last_name")
            address: str = request.POST.get("address")
            phone: str = request.POST.get("phone")
            with transaction.atomic():
                profile.first_name = first_name
                profile.last_name = last_name
                profile.address = address
                profile.phone = phone
                profile.save()
                order = Order.objects.create(
                    profile=profile,
                    total_price=Cart.get_total_price(profile)
                )
                for item in cart:
                    order_item = OrderItems.objects.create(
                        order=order,
                        product=item.product,
                        amount=item.amount
                    )
                    order_item.save()
                    item.delete()

        return HttpResponseRedirect('/mainapp/orders')


class OrdersView(TemplateView):
    template_name: str = "mainapp/orders.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(OrdersView, self).get_context_data(**kwargs)
        profile: Union[Type[Profile], str] = Profile.objects.filter(
            Q(user__username=self.request.user) | Q(
                session_id=self.request.session.session_key)
        ).first()
        orders: Dict[Type[Order], str] = Order.objects.filter(
            profile=profile
        )
        context['profile'] = profile
        context['orders'] = orders
        return context


class OrderListView(TemplateView):
    template_name: str = "mainapp/order_list.html"

    def get_context_data(self, pk: int = None, **kwargs: Any) -> Dict[str, Any]:
        context = super(OrderListView, self).get_context_data(**kwargs)
        context["order"] = Order.objects.get(id=pk)
        context["products"] = OrderItems.objects.filter(
            order__id=pk)
        return context
