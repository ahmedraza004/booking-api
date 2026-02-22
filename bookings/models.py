from django.db import models

# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='bookings')
    service_provider = models.ForeignKey('services.ServiceProvider', on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, default='pending') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return f"Booking {self.id} - {self.user.username} with {self.service_provider.name} for {self.service.name}"
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, default='pending') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return f"Payment {self.id} for Booking {self.booking.id} - {self.payment_status}"
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
class weeklyAvailability(models.Model):
    service_provider = models.ForeignKey('services.ServiceProvider', on_delete=models.CASCADE, related_name='weekly_availabilities')
    day_of_week = models.CharField(max_length=10) 
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return f"{self.service_provider.name} - {self.day_of_week} {self.start_time}-{self.end_time}"
    class Meta:
        verbose_name = 'Weekly Availability'
        verbose_name_plural = 'Weekly Availabilities'
        ordering = ['day_of_week', 'start_time']
class CalendarBlock(models.Model):
    service_provider = models.ForeignKey('services.ServiceProvider', on_delete=models.CASCADE, related_name='booking_calendar_blocks')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    def __str__(self):
        return f"{self.service_provider.name} - {self.date} {self.start_time}-{self.end_time} (Blocked)"
    class Meta:
        verbose_name = 'Booking Calendar Block'
        verbose_name_plural = 'Booking Calendar Blocks'
        ordering = ['date', 'start_time']