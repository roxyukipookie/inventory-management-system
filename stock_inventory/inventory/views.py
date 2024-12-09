from django.shortcuts import render, redirect,  get_object_or_404
from .forms import ProductForm, CategoryForm
from dashboard.models import Product, Category
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required

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

    # Apply category filter if provided
    if category_id:
        products = products.filter(category_id=category_id)

    # Product form handling
    form = ProductForm(request.POST or None, request.FILES or None, owner=owner)
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
        'total_products': total_products,
        'out_of_stock_items': out_of_stock_items,
        'low_stock_items': low_stock_items,
        'total_stock': total_stock,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'form': form,
        'form_has_errors': not form.is_valid()
    })


def history(request):
    return render(request, 'history.html')

def add_category(request):
    # Get the logged-in user
    user = request.user

    # Determine the owner (either the logged-in user or staff's owner)
    try:
        user_profile = UserProfile.objects.get(user=user)
        owner = user_profile.owner  # The owner linked to the staff
    except UserProfile.DoesNotExist:
        owner = user  # If no owner exists, assume the user is the owner

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.owner = owner  # Assign the logged-in owner
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('inventory')
        else:
            messages.error(request, 'There was an error adding the category. Please check the details.')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})

def delete_product(request, barcode):  
    print(f"Barcode received in the view: {barcode}")
    product = get_object_or_404(Product, barcode=barcode)  
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return HttpResponseRedirect(reverse('inventory'))

def edit_product(request, barcode):
    product = get_object_or_404(Product, barcode=barcode)
    if not product:
        messages.error(request, "Product not found.")
        return redirect('inventory')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            inputted_quantity = form.cleaned_data['quantity']
            product.quantity = inputted_quantity  # Update the quantity
            product.save(replenishing=True)  # Save with replenishing=True
            messages.success(request, 'Product updated successfully!')
            return redirect('inventory')
        else:
            messages.error(request, 'There was an error updating the product. Please check the details.')
            print(form.errors)
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})
