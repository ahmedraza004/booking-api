from django.shortcuts import render
from .models import Service, ServiceProvider, availability, CalenderBlock
from .serializer import ServiceSerializer, ServiceProviderSerializer, AvailabilitySerializer, CalendarBlockSerializer
from rest_framework import viewsets

# Create your views here.
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceProviderViewSet(viewsets.ModelViewSet):
    queryset = ServiceProvider.objects.all()
    serializer_class = ServiceProviderSerializer

class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = availability.objects.all()
    serializer_class = AvailabilitySerializer

class CalendarBlockViewSet(viewsets.ModelViewSet):
    queryset = CalenderBlock.objects.all()
    serializer_class = CalendarBlockSerializer