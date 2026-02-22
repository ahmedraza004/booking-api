from django.contrib import admin

from .models import Booking, Payment, weeklyAvailability, CalendarBlock
# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service_provider', 'service', 'date', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'service_provider__name', 'service__name')
    ordering = ('-created_at',)
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'payment_method', 'payment_status', 'created_at')
    list_filter = ('payment_status',)
    search_fields = ('booking__user__username', 'booking__service_provider__name', 'booking__service__name')
    ordering = ('-created_at',)
@admin.register(weeklyAvailability)
class WeeklyAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_provider', 'day_of_week', 'start_time', 'end_time', 'created_at')
    list_filter = ('day_of_week',)
    search_fields = ('service_provider__name',)
    ordering = ('day_of_week', 'start_time')
@admin.register(CalendarBlock)
class CalendarBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_provider', 'date', 'start_time', 'end_time', 'reason', 'created_at')
    list_filter = ('date',)
    search_fields = ('service_provider__name', 'reason')
    ordering = ('-created_at',)