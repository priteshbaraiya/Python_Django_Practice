from django.contrib import admin
from .models import Product, Sale
# Register your models here.

from django.contrib import admin
from .models import Product, Sale

# 1. Product Table ko dikhane ke liye
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'category', 'inventory_level') # Ye columns waha dikhenge
    search_fields = ('product_id', 'category') # Search bar bhi aa jayega

# 2. Sale Table ko dikhane ke liye
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'date', 'product_category', 'total_amount')
    list_filter = ('date', 'product_category') # Side me filter bhi aa jayega