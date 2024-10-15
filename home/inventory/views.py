from django.shortcuts import render, redirect
from .forms import ProductForm
from django.contrib import messages

def inventory(request):
    return render(request, 'html/inventory.html')

def invoice(request):
    return render(request, 'html/invoice.html')

def history(request):
    return render(request, 'html/history.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('inventory')
        else:
            messages.error(request, 'There was an error adding the product, Please check the details.')
    else:
        form = ProductForm()
    
    return render(request, 'html/add_product.html', {'form': form})