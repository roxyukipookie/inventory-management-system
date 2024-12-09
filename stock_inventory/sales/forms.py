from django import forms
from dashboard.models import Product
import random

class UpdateSalesForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sold_quantity']

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'sold_quantity' : forms.NumberInput(attrs={'class': 'form-control', 'min': 0})
        }

        labels = {
            'name' : 'Product Name', 
            'sold_quantity' : 'Quantity Sold'
        }

# Sales_terminal
class SalesTerminalForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1, initial=1, label="Quantity")