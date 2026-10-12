from django.db import models
from django.conf import settings
from catalog.models import Product, ProductVariant

class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        ADD = 'ADD', 'Add Stock'
        REMOVE = 'REMOVE', 'Remove Stock'
        DAMAGED = 'DAMAGED', 'Damaged Stock'
        LOST = 'LOST', 'Lost Stock'
        ADJUST = 'ADJUST', 'Stock Adjustment'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MovementType.choices)
    quantity = models.IntegerField(help_text="Positive for additions, negative for removals")
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} - {self.quantity} for {self.product.name}"

class SerialNumber(models.Model):
    class Status(models.TextChoices):
        IN_STOCK = 'IN_STOCK', 'In Stock'
        RESERVED = 'RESERVED', 'Reserved for Order'
        PACKED = 'PACKED', 'Packed'
        SOLD = 'SOLD', 'Sold / Dispatched'
        DAMAGED = 'DAMAGED', 'Damaged'
        RETURNED = 'RETURNED', 'Returned'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='serial_numbers')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True, related_name='serial_numbers')
    serial_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_STOCK, db_index=True)
    notes = models.TextField(blank=True, null=True)
    
    # Ideally link to OrderItem when reserved/packed/sold
    # order_item = models.ForeignKey('orders.OrderItem', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - S/N: {self.serial_number} ({self.status})"
