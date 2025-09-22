from django.db import models
from django.conf import settings

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    total_before_discount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_after_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    discount = models.ForeignKey("discounts.Discount", on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey("menu.MenuItem", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"
