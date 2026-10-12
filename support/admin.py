from django.contrib import admin
from .models import CustomerCareCase, CommunicationHistory

class CommunicationHistoryInline(admin.TabularInline):
    model = CommunicationHistory
    extra = 1

@admin.register(CustomerCareCase)
class CustomerCareCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'customer', 'status', 'is_urgent', 'assigned_assistant', 'created_at')
    list_filter = ('status', 'is_urgent', 'created_at')
    search_fields = ('subject', 'customer__username', 'guest_email', 'order__order_number')
    inlines = [CommunicationHistoryInline]
