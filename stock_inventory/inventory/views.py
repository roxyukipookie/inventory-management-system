from django.shortcuts import render, redirect,  get_object_or_404
from .forms import ProductForm, CategoryForm
from dashboard.models import Product, Category
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def inventory(request):
    query = request.GET.get('search', '')
    category_id = request.GET.get('category', None)

    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'inventory.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    })

def history(request):
    return render(request, 'history.html')

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
    
    return render(request, 'add_product.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('add_product')  # Redirect to the add product page or any other page
        else:
            messages.error(request, 'There was an error adding the category. Please check the details.')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})

def delete_product(request, barcode):  
    product = get_object_or_404(Product, barcode=barcode)  
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return HttpResponseRedirect(reverse('inventory'))

def edit_product(request, barcode):
    product = get_object_or_404(Product, barcode=barcode)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('inventory')
        else:
            messages.error(request, 'There was an error updating the product. Please check the details.')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})