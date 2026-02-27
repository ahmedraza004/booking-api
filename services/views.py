# views.py (Services app)

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Service, ServiceProvider, Availability, CalendarBlock
from .serializers import (
    ServiceSerializer, ServiceProviderSerializer,
    AvailabilitySerializer, CalendarBlockSerializer
)

# NOTE: add permissions if required (e.g., IsStaffOrReadOnly) like in your booking app.


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['active']
    ordering_fields = ['name', 'price', 'created_at']
    search_fields = ['name', 'description']


class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['active', 'available_services']
    ordering_fields = ['name', 'created_at']
    search_fields = ['name', 'email']


class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['service_provider', 'date']
    ordering_fields = ['date', 'start_time']


class CalendarBlockViewSet(viewsets.ModelViewSet):
    queryset = CalendarBlock.objects.all()
    serializer_class = CalendarBlockSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['service_provider', 'date']
    ordering_fields = ['date', 'start_time']