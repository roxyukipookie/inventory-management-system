# models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings  # Import settings to reference AUTH_USER_MODEL

from .managers import OwnerManager, StaffManager

class CustomUser(AbstractUser):
    # Additional fields for custom user model
    username = models.CharField(max_length=150, unique=True, default='default_username')

    role_choices = [
        ('Staff', 'Staff'),
        ('Owner', 'Owner'),
    ]
    
    role = models.CharField(max_length=10, choices=role_choices, default='Staff')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Owners will be inactive by default

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL here
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return self.user.username

class Owner(CustomUser):
    objects = OwnerManager()

    class Meta:
        proxy = True
        verbose_name = "Owner"
        verbose_name_plural = "Owner"

class Staff(CustomUser):
    objects = StaffManager()

    class Meta:
        proxy = True
        verbose_name = "Staff"
        verbose_name_plural = "Staff"