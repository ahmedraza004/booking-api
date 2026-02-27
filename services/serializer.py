# serializers.py (Services app)

from rest_framework import serializers
from .models import Service, ServiceProvider, Availability, CalendarBlock


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price,', 'active', 'created_at', 'updated_at']


class ServiceProviderSerializer(serializers.ModelSerializer):
    # writable list of service IDs; also expose nested read for GET
    available_services = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), many=True, write_only=True
    )
    available_services_detail = ServiceSerializer(source='available_services', many=True, read_only=True)

    class Meta:
        model = ServiceProvider
        fields = [
            'id', 'name', 'email', 'phone_number', 'active',
            'available_services', 'available_services_detail',
            'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        services = validated_data.pop('available_services', [])
        obj = super().create(validated_data)
        if services:
            obj.available_services.set(services)
        return obj

    def update(self, instance, validated_data):
        services = validated_data.pop('available_services', None)
        obj = super().update(instance, validated_data)
        if services is not None:
            obj.available_services.set(services)
        return obj


class AvailabilitySerializer(serializers.ModelSerializer):
    # allow POST with provider id; include nested provider in reads
    service_provider = serializers.PrimaryKeyRelatedField(
        queryset=ServiceProvider.objects.all()
    )
    service_provider_detail = ServiceProviderSerializer(source='service_provider', read_only=True)

    class Meta:
        model = Availability
        fields = ['id', 'service_provider', 'service_provider_detail', 'date', 'start_time', 'end_time', 'created_at', 'updated_at']


class CalendarBlockSerializer(serializers.ModelSerializer):
    service_provider = serializers.PrimaryKeyRelatedField(
        queryset=ServiceProvider.objects.all()
    )
    service_provider_detail = ServiceProviderSerializer(source='service_provider', read_only=True)

    class Meta:
        model = CalendarBlock
        fields = ['id', 'service_provider', 'service_provider_detail', 'date', 'start_time', 'end_time', 'reason', 'created_at', 'updated_at']