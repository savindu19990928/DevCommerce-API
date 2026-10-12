from rest_framework import serializers
from .models import RecommendationTag

class RecommendationTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationTag
        fields = '__all__'
