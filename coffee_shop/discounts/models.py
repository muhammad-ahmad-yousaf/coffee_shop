from django.db import models

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
