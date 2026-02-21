from django.contrib import admin
from .models import Service, ServiceProvider, availability, CalenderBlock
# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'active', 'created_at')
    list_filter = ('active',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',) 
@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number', 'active', 'created_at')
    list_filter = ('active',)
    search_fields = ('name', 'email')
    ordering = ('-created_at',)
@admin.register(availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_provider', 'date', 'start_time', 'end_time', 'created_at')
    list_filter = ('date',)
    search_fields = ('service_provider__name',)
    ordering = ('-created_at',)
@admin.register(CalenderBlock)
class CalendarBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_provider', 'date', 'start_time', 'end_time', 'reason', 'created_at')
    list_filter = ('date',)
    search_fields = ('service_provider__name', 'reason')
    ordering = ('-created_at',)
    
