from decimal import Decimal
from menu.models import MenuItem

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

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
