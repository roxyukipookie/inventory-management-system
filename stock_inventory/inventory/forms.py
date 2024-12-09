from django import forms
from django.core.exceptions import ValidationError
from dashboard.models import Product
from .models import Category
import random

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Retrieve the owner from kwargs if passed
        owner = kwargs.pop('owner', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        
        # Filter the category queryset by the owner if an owner is provided
        if owner:
            self.fields['category'].queryset = Category.objects.filter(owner=owner)
    
    def clean(self):
        cleaned_data = super().clean()
        mfg_date = cleaned_data.get('mfg_date')
        exp_date = cleaned_data.get('exp_date')

        if mfg_date and exp_date and exp_date < mfg_date:
            self.add_error('exp_date', "Expiration date must be after the manufacturing date.")

        return cleaned_data
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        product = self.instance
        if Product.objects.filter(name=name).exclude(id=product.id).exists():
            raise forms.ValidationError("A product with this name already exists.")
        return name
    
    def clean_barcode(self):
        barcode = self.cleaned_data.get('barcode')
        product = self.instance
        if Product.objects.filter(barcode=barcode).exclude(id=product.id).exists():
            raise forms.ValidationError("A product with this barcode already exists.")
        if not barcode.isdigit():
            raise forms.ValidationError("The barcode must contain only numbers.")
        if len(barcode) != 12:
            raise forms.ValidationError("The barcode must be 12 digits long.")
        return barcode

    def clean_quantity(self):
            quantity = self.cleaned_data.get('quantity')
            if quantity < 0:
                raise forms.ValidationError("Quantity cannot be negative.")
            return quantity
    
    class Meta:
        model = Product
        fields = ['name', 'category', 'barcode', 'description', 'mfg_date', 'exp_date', 'quantity', 'price', 'alert_threshold', 'image'] #fields to display
        
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Product Name'}),
            'category' : forms.Select(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Barcode', 'inputmode': 'numeric'}),
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
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']  # Adjust fields as necessary

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category Name'}),
        }
        