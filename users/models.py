# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        STAFF = 'staff', 'Staff'
        USER = 'user', 'User'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER,
        db_index=True,
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, db_index=True)

    REQUIRED_FIELDS = ['email']  # keep as-is if username is the login field

    def save(self, *args, **kwargs):
        # Normalize case-insensitive unique fields
        if self.email:
            self.email = self.email.strip().lower()
        if self.username:
            self.username = self.username.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]