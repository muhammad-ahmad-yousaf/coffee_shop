from django.db import models
from django.utils import timezone

class Discount(models.Model):
    DISCOUNT_TYPES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
        ("item_specific", "Item Specific"),
    ]

    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    min_order_value = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    valid_from = models.DateTimeField(blank=False)
    valid_to = models.DateTimeField(blank=False)
    max_uses = models.IntegerField(null=True, blank=True)
    max_uses_per_customer = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    specific_items = models.ManyToManyField("menu.MenuItem", blank=True, related_name="discounts")

    def __str__(self):
        return self.name


    def is_valid(self, user, cart_total, cart_items_count):
        if not self.is_active:
            return False

        now = timezone.now()
        if self.valid_from > now or self.valid_to < now:
            return False

        if self.min_order_value and cart_total < self.min_order_value:
            return False

        if self.max_uses is not None:
            used_count = self.order_set.count()
            if used_count >= self.max_uses:
                return False

        if self.max_uses_per_customer is not None:
            used_by_user = self.order_set.filter(customer=user).count()
            if used_by_user >= self.max_uses_per_customer:
                return False

        if self.type == "item_specific":
            required_items = self.specific_items.all()
            if not required_items.intersection(cart_items_count.keys()):
                return False

        return True
