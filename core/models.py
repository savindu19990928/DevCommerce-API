from django.db import models
from django.conf import settings
from orders.models import Order
import uuid

class AuditLog(models.Model):
    action_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    action_description = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    related_order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action_description} by {self.user.username if self.user else 'System'} at {self.timestamp}"
