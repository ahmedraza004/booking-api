from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    # Add any additional fields you want for your custom user model
    role = models.CharField(max_length=50, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'    
    