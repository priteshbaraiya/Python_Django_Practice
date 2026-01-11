from django.db import models
from django.utils import timezone
import time

class Product(models.Model):
    product_id = models.CharField(max_length=50, unique=True, editable=False, blank=True)
    name = models.CharField(max_length=100, default='Unnamed Product')
    category = models.CharField(max_length=100)
    inventory_level = models.IntegerField()  # Stock Quantity
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.product_id:
            # Generate a unique ID based on timestamp
            self.product_id = f'PROD-{int(time.time())}'
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Sale(models.Model):
    transaction_id = models.CharField(max_length=50)
    date = models.DateField()
    product_category = models.CharField(max_length=100) # This should ideally be a FK to Product
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale {self.transaction_id}"
