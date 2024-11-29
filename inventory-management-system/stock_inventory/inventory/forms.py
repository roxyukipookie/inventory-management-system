from django import forms
from django.core.exceptions import ValidationError
from dashboard.models import Product
from .models import Category
import random

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Check if the instance does not already have a barcode to avoid overwriting
        if not self.instance.pk:
            self.fields['barcode'].initial = self.generate_barcode()
            self.fields['barcode'].widget.attrs['readonly'] = True

    @staticmethod
    def generate_barcode():
        # Generate a random 8-digit barcode (ensure it's unique based on your requirements)
        return random.randint(100000000000, 999999999999)
    
    def clean(self):
        cleaned_data = super().clean()
        mfg_date = cleaned_data.get('mfg_date')
        exp_date = cleaned_data.get('exp_date')

        if mfg_date and exp_date and exp_date < mfg_date:
            self.add_error('exp_date', "Expiration date must be after the manufacturing date.")

        return cleaned_data
    
    class Meta:
        model = Product
        fields = ['name', 'category', 'barcode', 'description', 'mfg_date', 'exp_date', 'quantity', 'price', 'alert_threshold', 'image'] #fields to display
        
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Product Name'}),
            'category' : forms.Select(attrs={'class': 'form-control'}),
            'barcode' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Barcode', 'readonly': 'readonly'}),
            'description' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'mfg_date' : forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Mng. Date', 'type': 'date'}),
            'exp_date' : forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Exp. Date', 'type': 'date'}),
            'quantity' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Selling Price'}),
            'alert_threshold' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Low Stock Threshold'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'placeholder': 'Upload image'})
        }

        labels = {
            'name' : 'Product Name', 
            'category' : 'Category', 
            'barcode' : 'Barcode', 
            'description' : 'Description', 
            'mfg_date' : 'Mfg. Date', 
            'exp_date' : 'Exp. Date', 
            'quantity' : 'Initial Stock', 
            'price' : 'Selling Price (₱)', 
            'alert_threshold' : 'Low Stock Threshold',
            'image': 'Product Image',
        }
        
        def clean_quantity(self):
            quantity = self.cleaned_data.get('quantity')
            if quantity < 0:
                raise forms.ValidationError("Quantity cannot be negative.")
            return quantity
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']  # Adjust fields as necessary

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category Name'}),
        }
        