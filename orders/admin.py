from django.contrib import admin
from django.utils import timezone
from .models import Order, OrderItem, Warranty, Refund, Cart, CartItem, Coupon, PhoneCallRequest

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OverdueOrderFilter(admin.SimpleListFilter):
    title = 'overdue status'
    parameter_name = 'overdue'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Overdue'),
            ('no', 'On Time'),
        )

    def queryset(self, request, queryset):
        today = timezone.now().date()
        exclude_statuses = [Order.Status.DELIVERED, Order.Status.CANCELLED, Order.Status.REFUNDED, Order.Status.RETURNED]
        if self.value() == 'yes':
            return queryset.filter(estimated_arrival_date__lt=today).exclude(status__in=exclude_statuses)
        if self.value() == 'no':
            return queryset.exclude(estimated_arrival_date__lt=today).exclude(status__in=exclude_statuses)
        return queryset

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'guest_email', 'status', 'payment_status', 'total', 'estimated_arrival_date', 'is_overdue', 'requires_urgent_attention', 'created_at')
    list_filter = ('requires_urgent_attention', 'status', 'payment_status', OverdueOrderFilter, 'created_at')
    search_fields = ('order_number', 'guest_email', 'guest_phone', 'user__username')
    inlines = [OrderItemInline]

@admin.register(Warranty)
class WarrantyAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'serial_number', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('serial_number__serial_number', 'order_item__order__order_number')

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'status', 'initiated_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__order_number',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at')
    inlines = [CartItemInline]



@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'active', 'valid_from', 'valid_until')
    list_filter = ('active',)
    search_fields = ('code',)

@admin.register(PhoneCallRequest)
class PhoneCallRequestAdmin(admin.ModelAdmin):
    list_display = ('order', 'phone_number', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('order__order_number', 'phone_number')
