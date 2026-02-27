from django.db import models
from django.db.models import Q, F


class Booking(models.Model):
    # Status choices
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELED = 'canceled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELED, 'Canceled'),
    ]

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='bookings')
    service_provider = models.ForeignKey('services.ServiceProvider', on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='bookings')

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['service_provider', 'date']),
            models.Index(fields=['user', 'date']),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(start_time__lt=F('end_time')),
                name='booking_start_before_end'
            ),
        ]

    def __str__(self) -> str:
        return f"Booking {self.id} - {self.user} with {self.service_provider} for {self.service}"


class Payment(models.Model):
    # Payment method/status choices (extend as needed)
    METHOD_CARD = 'card'
    METHOD_CASH = 'cash'
    METHOD_STRIPE = 'stripe'
    METHOD_CHOICES = [
        (METHOD_CARD, 'Card'),
        (METHOD_CASH, 'Cash'),
        (METHOD_STRIPE, 'Stripe'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_SUCCEEDED = 'succeeded'
    STATUS_FAILED = 'failed'
    STATUS_REFUNDED = 'refunded'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SUCCEEDED, 'Succeeded'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_REFUNDED, 'Refunded'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payment_status']),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(amount__gt=0),
                name='payment_amount_positive'
            ),
        ]

    def __str__(self) -> str:
        return f"Payment {self.id} for Booking {self.booking_id} - {self.payment_status}"


class WeeklyAvailability(models.Model):
    """
    Weekly recurring availability windows for a provider.
    day_of_week: 0=Monday ... 6=Sunday
    """
    MON, TUE, WED, THU, FRI, SAT, SUN = range(7)
    DOW_CHOICES = [
        (MON, 'Monday'), (TUE, 'Tuesday'), (WED, 'Wednesday'),
        (THU, 'Thursday'), (FRI, 'Friday'), (SAT, 'Saturday'), (SUN, 'Sunday'),
    ]

    service_provider = models.ForeignKey('services.ServiceProvider', on_delete=models.CASCADE, related_name='weekly_availabilities')
    day_of_week = models.PositiveSmallIntegerField(choices=DOW_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Weekly Availability'
        verbose_name_plural = 'Weekly Availabilities'
        ordering = ['day_of_week', 'start_time']
        unique_together = [('service_provider', 'day_of_week', 'start_time', 'end_time')]
        indexes = [
            models.Index(fields=['service_provider', 'day_of_week']),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(start_time__lt=F('end_time')),
                name='weekly_availability_start_before_end'
            ),
        ]

    def __str__(self) -> str:
        return f"{self.service_provider} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"


class CalendarBlock(models.Model):
    """
    One-off block for a specific date/time window (vacation, maintenance, etc.).
    """
    service_provider = models.ForeignKey('services.ServiceProvider', on_delete=models.CASCADE, related_name='booking_calendar_blocks')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Booking Calendar Block'
        verbose_name_plural = 'Booking Calendar Blocks'
        ordering = ['date', 'start_time']
        indexes = [
            models.Index(fields=['service_provider', 'date']),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(start_time__lt=F('end_time')),
                name='calendar_block_start_before_end'
            ),
        ]

    def __str__(self) -> str:
        return f"{self.service_provider} - {self.date} {self.start_time}-{self.end_time} (Blocked)"
