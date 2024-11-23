from django import forms
from .models import CustomUser, Role
import re

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role', "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate the role choices from the Role model
        self.fields['role'].queryset = Role.objects.all()

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if any(char.isdigit() for char in first_name):
            raise forms.ValidationError("First name cannot contain numbers.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if any(char.isdigit() for char in last_name):
            raise forms.ValidationError("Last name cannot contain numbers.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Invalid email address.")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
    
    def clean_role(self):
        role = self.cleaned_data.get("role")
        if not role:
            role, _ = Role.objects.get_or_create(name="Guest")  # Default role
        return role
