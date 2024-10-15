from django import forms
from .models import AddProduct

class ProductForm(forms.ModelForm):
    class Meta:
        model = AddProduct
        fields = ['name', 'category', 'quantity', 'whole_sale', 'retail_sale']
        
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'category' : forms.Select(attrs={'class': 'form-contorl'}),
            'quantity' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'whole_sale' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Whole Sale Price'}),
            'retail_sale' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Retail Sale Price'}),
        }

        labels = {
            'name': 'Product Name',
            'category': 'Category',
            'quantity': 'Quantity',
            'whole_sale': 'Whole Sale Price (₱)',
            'retail_sale': 'Retail Sale Price (₱)',
        }

        def clean_retail(self):
            retail = self.cleaned_data.get('retail_sale')
            if retail <= 0:
                raise forms.ValidationError("Retail price must be greater then zero")
            return retail
        
        def clean_whole(self):
            whole = self.cleaned_data.get('whole_sale')
            retail = self.cleaned_data.get('retail_sale')
            if whole > retail:
                raise forms.ValidationError("Whole price must not higher than retail price.")
            return whole
        
        def clean_quantity(self):
            quantity = self.cleaned_data.get('quantity')
            if quantity < 0:
                raise forms.ValidationError("Quantity cannot be negative.")
            return quantity
