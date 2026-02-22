from rest_framework import serializers
from .models import Booking, Payment, CalendarBlock, weeklyAvailability
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'service_provider', 'service', 'date', 'start_time', 'end_time', 'status', 'created_at', 'updated_at']
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'payment_method', 'payment_status', 'created_at', 'updated_at']
class CalendarBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarBlock
        fields = ['id', 'service_provider', 'date', 'start_time', 'end_time', 'reason', 'created_at', 'updated_at'] 
class WeeklyAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = weeklyAvailability
        fields = ['id', 'service_provider', 'day_of_week', 'start_time', 'end_time', 'created_at', 'updated_at']