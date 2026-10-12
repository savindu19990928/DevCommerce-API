from rest_framework import serializers
from .models import CustomerCareCase, CommunicationHistory

class CommunicationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationHistory
        fields = '__all__'
        read_only_fields = ['sender']

class CustomerCareCaseSerializer(serializers.ModelSerializer):
    communications = CommunicationHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = CustomerCareCase
        fields = '__all__'
        read_only_fields = ['customer', 'assigned_assistant']
