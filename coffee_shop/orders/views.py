from django.shortcuts import render, redirect, get_object_or_404
from menu.models import MenuItem
from .models import Order, OrderItem
from .cart import Cart
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, item_id):
    cart = Cart(request)
    cart.add(item_id, quantity=1)
    return redirect("view-cart")

@login_required
def remove_from_cart(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    return redirect("view-cart")

@login_required
def view_cart(request):
    cart = Cart(request)
    return render(request, "orders/cart.html", {"cart": cart})

@login_required
def place_order(request):
    cart = Cart(request)
    if not cart.cart:
        return redirect("menu-list")

    order = Order.objects.create(
        customer=request.user,
        total_before_discount=cart.get_total_price(),
        discount_amount=0,  # discount logic comes later
        total_after_discount=cart.get_total_price(),
    )

    for item in cart:
        OrderItem.objects.create(
            order=order,
            menu_item=item["item"],
            quantity=item["quantity"],
            price=item["item"].price,
        )

    cart.clear()
    return redirect("order-history")

@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by("-order_date")
    return render(request, "orders/order_history.html", {"orders": orders})
