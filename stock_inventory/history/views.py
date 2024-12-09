from django.shortcuts import render
from dashboard.models import Product
from accounts.models import UserProfile
from .models import Sales_History

def history(request):
    sales_history = Sales_History.objects.all().order_by('-sale_time')
    # Get the logged-in user
    user = request.user

    # Check if the logged-in user is staff and has an associated owner
    try:
        user_profile = UserProfile.objects.get(user=user)
        owner = user_profile.owner  # Get the owner of the logged-in staff
    except UserProfile.DoesNotExist:
        owner = None

    # If the user is a staff member, show products of their associated owner
    if owner:
        products = Product.objects.filter(owner=owner)
        recently_added_products = products.order_by('-created_at')
    else:
        # If the user is an owner, show their own products
        products = Product.objects.filter(owner=user)
        recently_added_products = products.order_by('-created_at')

    context = {
        'recently_added_products': recently_added_products,
        'sales_history': sales_history,
    }

    return render(request, 'history.html', context)
