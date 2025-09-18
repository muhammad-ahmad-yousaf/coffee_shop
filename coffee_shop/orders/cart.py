from decimal import Decimal
from menu.models import MenuItem
from discounts.models import Discount
from django.utils import timezone

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart
        self.discount_id = self.session.get("discount_id")

    def add(self, menu_item_id, quantity=1):
        menu_item_id = str(menu_item_id)
        if menu_item_id not in self.cart:
            self.cart[menu_item_id] = {"quantity": 0}
        self.cart[menu_item_id]["quantity"] += quantity
        self.save()

    def remove(self, menu_item_id):
        menu_item_id = str(menu_item_id)
        if menu_item_id in self.cart:
            del self.cart[menu_item_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session["cart"] = {}
        self.session["discount_id"] = None
        self.save()

    def __iter__(self):
        item_ids = self.cart.keys()
        items = MenuItem.objects.filter(id__in=item_ids)
        for item in items:
            cart_item = self.cart[str(item.id)]
            cart_item["item"] = item
            cart_item["total_price"] = item.price * cart_item["quantity"]
            yield cart_item

    def get_total_price(self):
        return sum(item["item"].price * item["quantity"] for item in self.__iter__())

    def apply_discount(self, discount):
        self.session["discount_id"] = discount.id
        self.save()
    def get_discount(self, user=None):
        if self.discount_id:
            try:
                discount = Discount.objects.get(id=self.discount_id)
                cart_total = self.get_total_price()
                cart_items_count = {item["item"]: item["quantity"] for item in self.__iter__()}
                
                if discount.is_valid(user, cart_total, cart_items_count):
                    return discount
            except Discount.DoesNotExist:
                return None
        return None

    def get_total_after_discount(self):
        total = self.get_total_price()
        discount = self.get_discount()
        if not discount:
            return total, Decimal(0)

        discount_amount = Decimal(0)

        if discount.type == "percentage":
            discount_amount = total * (discount.value / 100)
        elif discount.type == "fixed":
            discount_amount = min(discount.value, total)
        elif discount.type == "item_specific":
            for item in self.__iter__():
                if item["item"] in discount.specific_items.all():
                    discount_amount += item["item"].price * item["quantity"] * (discount.value / 100)

        return total - discount_amount, discount_amount
