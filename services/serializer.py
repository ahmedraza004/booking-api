from rest_framework import serializers
from .models import Service, ServiceProvider, availability, CalenderBlock

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'active', 'created_at', 'updated_at']
class ServiceProviderSerializer(serializers.ModelSerializer):
    available_services = ServiceSerializer(many=True, read_only=True)
    class Meta:
        model = ServiceProvider
        fields = ['id', 'name', 'email', 'phone_number', 'active', 'available_services', 'created_at', 'updated_at']            
class AvailabilitySerializer(serializers.ModelSerializer):
    service_provider = ServiceProviderSerializer(read_only=True)
    class Meta:
        model = availability
        fields = ['id', 'service_provider', 'date', 'start_time', 'end_time', 'created_at', 'updated_at']
class CalendarBlockSerializer(serializers.ModelSerializer):
    service_provider = ServiceProviderSerializer(read_only=True)
    class Meta:
        model = CalenderBlock
        fields = ['id', 'service_provider', 'date', 'start_time', 'end_time', 'reason', 'created_at', 'updated_at']