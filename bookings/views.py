from django.shortcuts import render
from .models import Booking, Payment, weeklyAvailability, CalendarBlock
from .serializer import BookingSerializer, PaymentSerializer,WeeklyAvailabilitySerializer, CalendarBlockSerializer
from rest_framework import viewsets

# Create your views here.
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class WeeklyAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = weeklyAvailability.objects.all()
    serializer_class = WeeklyAvailabilitySerializer

class CalendarBlockViewSet(viewsets.ModelViewSet):
    queryset = CalendarBlock.objects.all()
    serializer_class = CalendarBlockSerializer
    

