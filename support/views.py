from rest_framework import viewsets, permissions
from core.permissions import IsCustomerOrHasGranularPermission
from .models import CustomerCareCase, CommunicationHistory
from .serializers import CustomerCareCaseSerializer, CommunicationHistorySerializer

class CustomerCareCaseViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerCareCaseSerializer
    permission_classes = [IsCustomerOrHasGranularPermission]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'ASSISTANT']:
            return CustomerCareCase.objects.all()
        return CustomerCareCase.objects.filter(customer=user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class CommunicationHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = CommunicationHistorySerializer
    permission_classes = [IsCustomerOrHasGranularPermission]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'ASSISTANT']:
            return CommunicationHistory.objects.all()
        return CommunicationHistory.objects.filter(care_case__customer=user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, is_customer=(self.request.user.role == 'CUSTOMER'))
