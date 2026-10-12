from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action_id', 'action_description', 'user', 'related_order', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('action_description', 'user__username', 'related_order__order_number')
