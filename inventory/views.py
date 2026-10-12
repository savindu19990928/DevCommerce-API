from rest_framework import viewsets, permissions
from .models import StockMovement, SerialNumber
from .serializers import StockMovementSerializer, SerialNumberSerializer

from core.permissions import HasGranularPermission

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [HasGranularPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class SerialNumberViewSet(viewsets.ModelViewSet):
    queryset = SerialNumber.objects.all()
    serializer_class = SerialNumberSerializer
    permission_classes = [HasGranularPermission]
    filterset_fields = ['status', 'product']
