# accounts/managers.py
from django.contrib.auth.models import BaseUserManager

class OwnerManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role='Owner')

class StaffManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role='Staff')