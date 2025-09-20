from django.db import models

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ("coffee", "Coffee"),
        ("pastry", "Pastry"),
        ("drink", "Drink"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to="menu_images/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} (${self.price})"
