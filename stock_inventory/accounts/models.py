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

    is_owner = models.BooleanField(default=False)
    owner = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='Staff')

    
    role = models.CharField(max_length=10, choices=role_choices, default='Staff')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Owners will be inactive by default

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Ensure `owner` is not required for Owner users
        if self.role == 'Owner':
            self.owner = None  # Clear the owner field for Owner users
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL here
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    owner = models.ForeignKey(CustomUser, related_name='staff', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    def is_staff(self):
        return self.owner is not None

    def is_owner(self):
        return self.owner is None

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