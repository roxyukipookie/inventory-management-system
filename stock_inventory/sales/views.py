from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from dashboard.models import Product, Category
from .models import SalesTerminal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .forms import SalesTerminalForm
from decimal import Decimal
import json

# Sales_terminal View
def sales_terminal(request):
    products_in_terminal = request.session.get("sales_terminal", [])
    categories = Category.objects.all()
    selected_category = request.GET.get("category")

    total_price = Decimal("0.00")

    for product in products_in_terminal:
        total_price += Decimal(product["price"] * product["quantity"])

    if selected_category:
        products = Product.objects.filter(category_id=selected_category)
    else:
        products = Product.objects.all()

    context = {
        "categories": categories,
        "selected_category": selected_category,
        "products": products,
        "sales_products": products_in_terminal,
        "total_price": total_price,
    }
    return render(request, "sales_terminal.html", context)

#Logic for product selection
@csrf_protect
def add_to_sales_terminal(request):
    if request.method == "POST":
        # Extract quantity and product details
        quantity = request.POST.get("quantity", "1")  # Default to "1" (string) to avoid NoneType error

        # Validate that quantity is a positive integer
        if not quantity.isdigit() or int(quantity) <= 0:
            quantity = 1
        else:
            quantity = int(quantity)   

        barcode = request.POST.get("barcode")
        # Fetch the product from the database using the barcode
        product = Product.objects.get(barcode=barcode)         

        product_name = request.POST.get("product_name")
        description = request.POST.get("description")
        price = request.POST.get("price")

        # Initialize sales terminal session if it doesn't exist
        if "sales_terminal" not in request.session:
            request.session["sales_terminal"] = []

        sales_terminal = request.session["sales_terminal"]

        # Convert price from Decimal to float
        price = float(product.price)

        # Check if the product already exists in the sales terminal
        product_exists = False
        for item in sales_terminal:
            if item["barcode"] == product.barcode:  # Check by unique barcode
                item["quantity"] += quantity
                product_exists = True
                break

        # If the product doesn't exist, add it to the session
        if not product_exists:
            sales_terminal.append({
                "name": product.name,
                "barcode": product.barcode,
                "description": product.description,
                "price": price,
                "quantity": quantity,
            })

        # Mark the session as modified and redirect
        request.session.modified = True
        return redirect("sales_terminal")

    return redirect("sales_terminal")


# CLear Btn
def clear_sales_terminal(request):
    # Remove sales terminal data from the session
    if "sales_terminal" in request.session:
        del request.session["sales_terminal"]
    return redirect("sales_terminal")  # Redirect back to the sales terminal page

# Total Btn
def process_total(request):
    # Ensure sales_terminal exists in session
    sales_terminal = request.session.get("sales_terminal", [])
    if not sales_terminal:
        messages.error(request, "Sales terminal is empty. Cannot process total.")
        return redirect("sales_terminal")

    # Loop through sales_terminal and update database quantities
    for item in sales_terminal:
        try:
            # Find the product in the database by barcode
            product = Product.objects.get(barcode=item["barcode"])
            
            # Check if enough quantity is available
            if product.quantity >= item["quantity"]:
                product.quantity -= item["quantity"]
                product.save()
            else:
                messages.error(
                    request,
                    f"Not enough stock for {product.name}. Available: {product.quantity}, Required: {item['quantity']}"
                )
                return redirect("sales_terminal")
        except Product.DoesNotExist:
            messages.error(request, f"Product with barcode {item['barcode']} not found.")
            return redirect("sales_terminal")
    
    # Clear sales terminal after processing
    del request.session["sales_terminal"]
    request.session.modified = True

    messages.success(request, "Sales terminal processed successfully!")
    return redirect("sales_terminal")