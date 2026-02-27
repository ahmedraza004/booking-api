# models.py (Services app) – adjust class names + add constraints/indexes

from django.db import models
from django.db.models import Q, F


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.name


class ServiceProvider(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    active = models.BooleanField(default=False)
    available_services = models.ManyToManyField(Service, related_name='providers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Service Provider'
        verbose_name_plural = 'Service Providers'

    def __str__(self):
        return self.name


class Availability(models.Model):  # renamed from availability
    service_provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE, related_name='availabilities'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Availability'
        verbose_name_plural = 'Availabilities'
        ordering = ['date', 'start_time']
        indexes = [
            models.Index(fields=['service_provider', 'date']),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(start_time__lt=F('end_time')),
                name='availability_start_before_end',
            ),
        ]

    def __str__(self):
        return f"{self.service_provider.name} - {self.date} {self.start_time}-{self.end_time}"


class CalendarBlock(models.Model):  # renamed from CalenderBlock
    service_provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE, related_name='calendar_blocks'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Calendar Block'
        verbose_name_plural = 'Calendar Blocks'
        ordering = ['date', 'start_time']
        indexes = [
            models.Index(fields=['service_provider', 'date']),
        ]
        constraints = [
            models.CheckConstraint(
                check=Q(start_time__lt=F('end_time')),
                name='calendar_block_start_before_end',
            ),
        ]

    def __str__(self):
        return f"{self.service_provider.name} - {self.date} {self.start_time}-{self.end_time} (Blocked)"