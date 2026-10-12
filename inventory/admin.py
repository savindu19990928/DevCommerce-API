from django.contrib import admin
from .models import StockMovement, SerialNumber

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'created_by', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('product__name', 'notes')

@admin.register(SerialNumber)
class SerialNumberAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'product', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('serial_number', 'product__name')
