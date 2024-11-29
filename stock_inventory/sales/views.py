from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from dashboard.models import Product, Category
from .models import SalesTerminal
from django.http import JsonResponse
import json

def sales(request):
    return render(request, 'sales.html')

def sales_management(request):
    print(Product.objects.all())
    products = Product.objects.all()
    print(products)

    recently_added_products = Product.objects.order_by('-created_at')

    context = {
        'recently_added_products' : recently_added_products

    }

    return render(request, 'sales_management.html', context)

def sales_terminal(request):
    query = request.GET.get('search', '')
    category_id = request.GET.get('category', None)

    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'sales_terminal.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    })

def update_quantities(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            products = data.get("products", [])
            errors = []

            for product_data in products:
                barcode = product_data.get("barcode")
                quantity = product_data.get("quantity")

                if not barcode or not quantity:
                    continue  # Skip invalid entries

                # Fetch the product by barcode
                product = Product.objects.filter(barcode=barcode).first()
                if product:
                    if product.quantity >= quantity:
                        # Create a sale record
                        total_price = product.price * quantity
                        sale = SalesTerminal.objects.create(
                            product=product,
                            quantity_sold=quantity,
                            total_price=total_price
                        )

                        # Deduct stock and update sold quantities
                        product.sold_quantity += quantity
                        product.total_sold_quantity += quantity
                        product.quantity -= quantity
                        product.save()
                    else:
                        errors.append(f"Insufficient stock for {product.name} (Available: {product.quantity}, Requested: {quantity})")
                else:
                    errors.append(f"Product with barcode {barcode} not found.")

            if errors:
                return JsonResponse({"success": False, "errors": errors})

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})