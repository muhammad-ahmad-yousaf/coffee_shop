from django.shortcuts import render, redirect, get_object_or_404
from menu.models import MenuItem
from .models import Order, OrderItem
from .services.cart_service import CartService
from django.contrib.auth.decorators import login_required
from discounts.models import Discount
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib import messages



@login_required
def apply_discount(request, discount_id):
    cart = CartService(request)
    discount = get_object_or_404(Discount, id=discount_id, is_active=True)
    cart.apply_discount(discount)
    return redirect("view-cart")

@require_POST
@login_required
def add_to_cart(request, item_id):
    cart = CartService(request)
    quantity = int(request.POST.get("quantity", 1))
    cart.add(item_id, quantity)
    messages.success(request, "Item added to cart successfully!")
    return redirect("view-cart")

@login_required
def remove_from_cart(request, item_id):
    cart = CartService(request)
    cart.remove(item_id)
    messages.warning(request, "Item Deleted from cart!!!")
    return redirect("view-cart")

@login_required
def view_cart(request):
    cart = CartService(request)
    discounts = Discount.objects.filter(is_active=True)

    valid_discounts = []
    for d in discounts:
        if d.is_valid(request.user, cart.get_total_price(), {i["item"]: i["quantity"] for i in cart}):
            valid_discounts.append(d)

    return render(request, "orders/cart.html", {"cart": cart, "discounts": valid_discounts})



@login_required
def place_order(request):
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

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by("-order_date")
    return render(request, "orders/order_history.html", {"orders": orders})
