from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Custom Manager for CustomUser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Ensure the superuser is assigned an Admin role
        role = Role.objects.get(name="Admin")
        extra_fields['role'] = role

        return self.create_user(email, password, **extra_fields)
    
# Custom User Model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey("Role", on_delete=models.SET_NULL, null=True, blank=True)

    username = None  # Remove the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# Role Model
class Role(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        related_name='roles',
        null=True,  # Allows empty values
        blank=True,  # Allows skipping input in forms
    )

    def __str__(self):
        return self.name


# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    additional_info = models.TextField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.email}"
