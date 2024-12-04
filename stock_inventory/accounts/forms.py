# forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from .models import CustomUser

# Custom validator for names (no numbers allowed)
def validate_name(value):
    if any(char.isdigit() for char in value):
        raise ValidationError("Name should not contain numbers.")

class RegistrationForm(forms.ModelForm):
    # Add the MinLengthValidator to the password field
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[MinLengthValidator(8)]  # Ensure password is at least 8 characters long
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'role', 'profile_picture']

    # Custom validation for first_name and last_name
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        validate_name(first_name)  # Apply custom name validator
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        validate_name(last_name)  # Apply custom name validator
        return last_name

    # Custom validation for password length
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Set the password correctly
        if commit:
            user.save()
        return user