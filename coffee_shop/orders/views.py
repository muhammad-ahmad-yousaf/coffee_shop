from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from menu.models import MenuItem
from .models import Order, OrderItem
from .services.cart_service import CartService
from discounts.models import Discount

class ApplyDiscountView(LoginRequiredMixin, View):
    def get(self, request, discount_id):
        cart = CartService(request)
        discount = get_object_or_404(Discount, id=discount_id, is_active=True)
        cart.apply_discount(discount)
        return redirect("view-cart")

@method_decorator(require_POST, name="dispatch")
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart = CartService(request)
        quantity = int(request.POST.get("quantity",1))
        cart.add(item_id,quantity)
        messages.success(request, "Item added to cart successfully!")
        return redirect("menu-list")

class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, item_id):
        cart = CartService(request)
        cart.remove(item_id)
        messages.warning(request, "Item Deleted from cart !!")
        return redirect("view-cart")

class ViewCartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = CartService(request)
        discounts = Discount.objects.filter(is_active=True)

        valid_discounts = [
            d for d in discounts if d.is_valid(
                request.user,
                cart.get_total_price(),
                {i["item"]: i["quantity"] for i in cart},
            )
        ]

        return render(request, "orders/cart.html", {"cart": cart, "discounts": valid_discounts})

class PlaceOrderView(LoginRequiredMixin, View):
    def get(self, request):
        cart = CartService(request)
        if not cart.cart:
            return redirect("menu-list")

        discount = cart.get_discount(user=request.user)
        total_after, discount_amount = cart.get_total_after_discount()

        order = Order.objects.create(
            customer=request.user,
            total_before_discount=cart.get_total_price(),
            discount=discount,
            discount_amount=discount_amount,
            total_after_discount=total_after,
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                menu_item=item["item"],
                quantity=item["quantity"],
                price=item["item"].price,
            )

        cart.clear()
        messages.success(request, f"Your Order No. {order.id} is Placed successfully!")
        return redirect("order-history")

class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/order_history.html"
    context_object_name = "orders"
    paginate_by = 5

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by("-order_date")
