from rest_framework import serializers
from .models import Booking, Payment, CalendarBlock, WeeklyAvailability


class BookingSerializer(serializers.ModelSerializer):
    # expose user as read-only; bind in view via perform_create
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'service_provider', 'service',
            'date', 'start_time', 'end_time', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Conflict checks:
        - start < end
        - inside WeeklyAvailability for the weekday
        - not overlapping any CalendarBlock
        - not overlapping any CONFIRMED booking
        """
        start = data.get('start_time')
        end = data.get('end_time')
        date = data.get('date')
        provider = data.get('service_provider')

        if not (start and end and date and provider):
            return data  # DRF will raise field-specific errors if absent

        if not (start < end):
            raise serializers.ValidationError("start_time must be before end_time.")

        # Weekly availability check
        weekday = date.weekday()  # 0=Mon ... 6=Sun
        avail_exists = WeeklyAvailability.objects.filter(
            service_provider=provider,
            day_of_week=weekday,
            start_time__lte=start,
            end_time__gte=end
        ).exists()
        if not avail_exists:
            raise serializers.ValidationError("Requested time is outside provider weekly availability.")

        # Calendar block overlap
        blocks = CalendarBlock.objects.filter(
            service_provider=provider,
            date=date
        )
        for b in blocks:
            if max(start, b.start_time) < min(end, b.end_time):
                raise serializers.ValidationError("Requested time overlaps a calendar block.")

        # Existing confirmed bookings overlap
        existing = Booking.objects.filter(
            service_provider=provider,
            date=date,
            status=Booking.CONFIRMED
        )
        for bk in existing:
            if max(start, bk.start_time) < min(end, bk.end_time):
                raise serializers.ValidationError("Requested time overlaps another confirmed booking.")

        return data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'payment_method', 'payment_status', 'created_at', 'updated_at']
        read_only_fields = ['payment_status', 'created_at', 'updated_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("amount must be greater than 0.")
        return value


class CalendarBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarBlock
        fields = ['id', 'service_provider', 'date', 'start_time', 'end_time', 'reason', 'created_at', 'updated_at']


class WeeklyAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyAvailability
        fields = ['id', 'service_provider', 'day_of_week', 'start_time', 'end_time', 'created_at', 'updated_at']