from django.db import models
from django.conf import settings
from orders.models import Order

class CustomerCareCase(models.Model):
    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        RESOLVED = 'RESOLVED', 'Resolved'
        CLOSED = 'CLOSED', 'Closed'

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_cases')
    guest_email = models.EmailField(blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_cases')
    
    assigned_assistant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_cases')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, db_index=True)
    
    subject = models.CharField(max_length=255)
    is_urgent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Case #{self.id} - {self.subject}"

class CommunicationHistory(models.Model):
    care_case = models.ForeignKey(CustomerCareCase, on_delete=models.CASCADE, related_name='communications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_customer = models.BooleanField(default=False)
    message = models.TextField()
    channel = models.CharField(max_length=50, default='CHAT', help_text="e.g., CHAT, EMAIL, WHATSAPP, SYSTEM_NOTE")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comm #{self.id} for Case #{self.care_case_id}"
