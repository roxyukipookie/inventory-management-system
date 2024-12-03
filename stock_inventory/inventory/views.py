from django.shortcuts import render, redirect,  get_object_or_404
from .forms import ProductForm, CategoryForm
from dashboard.models import Product, Category
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from accounts.models import UserProfile

def inventory(request):
    query = request.GET.get('search', '')
    category_id = request.GET.get('category', None)

    # Get the logged-in user
    user = request.user

    # Get the owner of the logged-in staff, if applicable
    try:
        user_profile = UserProfile.objects.get(user=user)
        owner = user_profile.owner  # The owner linked to the staff
    except UserProfile.DoesNotExist:
        # If the user is not staff or no owner exists, assume the user is the owner
        owner = user

    # Filter products by the owner (either the logged-in user or the staff's owner)
    products = Product.objects.filter(owner=owner)

    # Calculate the required variables using the 'quantity' field
    total_products = products.count()
    out_of_stock_items = products.filter(quantity=0).count()  # Adjusted to use 'quantity'
    low_stock_items = products.filter(quantity__lte=5).count()  # Adjusted to use 'quantity'
    total_stock = sum(product.quantity for product in products)  # Adjusted to use 'quantity'

    # Filter categories associated with the owner's products
    categories = Category.objects.filter(products__owner=owner).distinct()

    # Apply search query filter if provided
    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(category_id=category_id)

    # Product form handling
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            # Assign the logged-in user as the owner of the new product
            product = form.save(commit=False)
            product.owner = owner  # Handle staff case
            product.save()
            messages.success(request, "Product added successfully.")
            return redirect('inventory')
        else:
            messages.error(request, "Please correct the errors in the form.")

    return render(request, 'new_inventory.html', {
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