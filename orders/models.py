from django.db import models
from django.conf import settings
from django.utils import timezone
from catalog.models import Product, ProductVariant
from inventory.models import SerialNumber
import uuid

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAYMENT_PROCESSING = 'PAYMENT_PROCESSING', 'Payment Processing'
        PAID = 'PAID', 'Paid'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        PACKING = 'PACKING', 'Packing'
        READY_FOR_DISPATCH = 'READY_FOR_DISPATCH', 'Ready for Dispatch'
        IN_TRANSIT = 'IN_TRANSIT', 'In Transit'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'
        REFUNDED = 'REFUNDED', 'Refunded'
        PARTIALLY_REFUNDED = 'PARTIALLY_REFUNDED', 'Partially Refunded'
        RETURNED = 'RETURNED', 'Returned'

    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    order_number = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Guest Info
    guest_email = models.EmailField(blank=True, null=True)
    guest_phone = models.CharField(max_length=20, blank=True, null=True)
    guest_name = models.CharField(max_length=150, blank=True, null=True)

    # Totals
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Status
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING, db_index=True)
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.PENDING, db_index=True)
    payment_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    
    requires_urgent_attention = models.BooleanField(default=False)
    
    # Dates
    estimated_arrival_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Tracking
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    courier = models.CharField(max_length=100, blank=True, null=True)
    
    # Secure links tokens
    guest_tracking_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    receipt_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    @property
    def is_overdue(self):
        if not self.estimated_arrival_date:
            return False
        return self.estimated_arrival_date < timezone.now().date() and self.status not in [self.Status.DELIVERED, self.Status.CANCELLED, self.Status.REFUNDED, self.Status.RETURNED]

    def __str__(self):
        return f"Order {self.order_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Optional assigned serial numbers
    serial_numbers = models.ManyToManyField(SerialNumber, blank=True, related_name='order_items')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.order_number})"

class Warranty(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        EXPIRED = 'EXPIRED', 'Expired'
        VOIDED = 'VOIDED', 'Voided'

    order_item = models.OneToOneField(OrderItem, on_delete=models.CASCADE, related_name='warranty')
    serial_number = models.ForeignKey(SerialNumber, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    
    def __str__(self):
        return f"Warranty for {self.order_item}"

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refunds')
    items = models.ManyToManyField(OrderItem, blank=True, related_name='refunds')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, default='COMPLETED')
    initiated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund for Order {self.order.order_number} - {self.amount}"

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"



class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"

class PhoneCallRequest(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='phone_call_requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    reason = models.TextField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Call Request for Order {self.order.order_number} ({self.phone_number})"
