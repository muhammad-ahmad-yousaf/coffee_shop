from django.contrib import admin
from .models import Discount

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "value", "is_active", "valid_from", "valid_to")
    list_filter = ("type", "is_active")
    search_fields = ("name", "description")