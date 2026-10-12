from rest_framework import viewsets, permissions
from core.permissions import IsAdmin
from .models import RecommendationTag
from .serializers import RecommendationTagSerializer

class RecommendationTagViewSet(viewsets.ModelViewSet):
    queryset = RecommendationTag.objects.all()
    serializer_class = RecommendationTagSerializer
    permission_classes = [IsAdmin]
