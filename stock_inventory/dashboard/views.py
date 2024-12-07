import traceback
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.db.models import F, Sum 
from .models import Product, Notification
from inventory.models import Category
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
import logging
from accounts.models import UserProfile 
from accounts.models import CustomUser
import django_excel as excel
import pyexcel
import pandas as pd

@login_required(login_url='/accounts/login/')
def dashboard_view(request):
    user = request.user
    user_role = 'staff' if UserProfile.objects.filter(user=request.user, owner__isnull=False).exists() else 'owner'

    # Determine the owner of the logged-in user
    try:
        user_profile = UserProfile.objects.get(user=user)
        owner = user_profile.owner  # The owner linked to the staff
    except UserProfile.DoesNotExist:
        owner = user  # If the user is not staff, they are the owner

    
    products = Product.objects.filter(owner=owner) # Only get products owned by the determined owner

    # Data for the chart
    product_names = [product.name for product in products]
    remaining_quantities = [product.quantity for product in products]
    sold_quantities = [product.total_sold_quantity for product in products]  # Use cumulative sold quantity
    sales_by_category = (Product.objects.filter(owner=owner, category__isnull=False).values("category__name").annotate(total_sales=Sum("total_sold_quantity")).order_by("-total_sales"))   
    category_names = [item["category__name"] for item in sales_by_category]
    category_sales = [item["total_sales"] for item in sales_by_category]

    # Dashboard statistics
    all_products = products
    total_products = products.count()  # Count products owned by the owner
    total_stock = products.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    low_stock_items = products.filter(quantity__lt=F('alert_threshold')).count()
    out_of_stock_items = products.filter(quantity=0).count()
    top_products_sold = products.order_by('-total_sold_quantity')[:5]  # Top products by cumulative sales
    recently_added_products = products.order_by('-created_at')[:5]

    print(category_names, category_sales)

    # Context for rendering
    context = {
        'all_products': all_products,
        'total_products': total_products,
        'total_stock': total_stock,
        'low_stock_items': low_stock_items,
        'out_of_stock_items': out_of_stock_items,
        'top_products_sold': top_products_sold,
        'recently_added_products': recently_added_products,
        'product_names': product_names,
        'remaining_quantities': remaining_quantities,
        'sold_quantities': sold_quantities,
        'user_role': user_role,
        "category_names": json.dumps(category_names),  
        "category_sales": json.dumps(category_sales),
    }
    return render(request, 'dashboard.html', context)

def get_notifications(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
        owner = user_profile.owner
    except UserProfile.DoesNotExist:
        owner = user

    print(f"Owner: {owner}")

    # Filter notifications by the owner of the logged-in user
    notifications = Notification.objects.filter(owner=owner, is_read=False).order_by('-created_at')[:5]

    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'title': notification.title,
            'message': notification.message,
            'icon': notification.icon,
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'notification_type': notification.notification_type
        })

    return JsonResponse({
        'notifications': notifications_data,
    }, safe=False)



def export_products(request):
    user = request.user

    # Determine the owner of the logged-in user
    try:
        user_profile = UserProfile.objects.get(user=user)
        owner = user_profile.owner  # The owner linked to the staff
    except UserProfile.DoesNotExist:
        owner = user  # If the user is not staff, they are the owner

    products = Product.objects.filter(owner=owner).values(
        'name', 'quantity', 'price', 'sold_quantity', 'total_sales', 'mfg_date', 'exp_date', 'description'
    )
    df = pd.DataFrame(list(products))
    if df.empty:
        return HttpResponse("No products found for this owner.", status=404)

    # Response to generate an Excel file
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'

    #Export to excel
    df.to_excel(response, index=False, engine='openpyxl')

    return response

def role_management_view(request):
    return render(request, 'role_management.html')

@login_required
def user_management_view(request):
    User = get_user_model()

    if request.user.is_owner:
        # Fetch only users who are staff and linked to the current owner
        users = User.objects.filter(role='Staff', owner=request.user)
        user_count = users.count()
    else:
        # If the user is not an owner, display an empty list or show an error
        users = []
        user_count = 0
    
    context = {
        'users': users,
        'user_count': user_count,
    }
    return render(request, 'user_management.html', context)

@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role', '').lower()
        profile_picture = request.FILES.get('profile_picture')  # Profile picture upload

        try:
            # Step 1: Create the new user
            user = CustomUser.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.set_password(password)

            # Step 2: Create the UserProfile with the role and profile picture
            if not UserProfile.objects.filter(user=user).exists():
                profile = UserProfile.objects.create(
                    user=user,
                    profile_picture=profile_picture  # Save profile picture
                )

                # Set the logged-in user as the owner for this new user
                user.owner = request.user  # Set the `owner` field in the `CustomUser` model
                profile.owner = request.user  # Also set in UserProfile (just for consistency)
                user.save()  # Save the user with the owner set
                profile.save()  # Save the profile

                # Set role based on form input
                if role == 'staff':
                    user.is_staff = False
                    user.is_superuser = False
                    profile.role = 'staff'
                elif role == 'owner':
                    user.is_superuser = False
                    user.is_staff = False
                    profile.role = 'owner'
                else:
                    user.is_staff = False
                    user.is_superuser = False
                    profile.role = 'n/a'

                user.save()  # Save updated user permissions
                profile.save()  # Save updated profile

            return JsonResponse({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': profile.role.capitalize(),
                    'profile_picture': profile.profile_picture.url if profile.profile_picture else None
                }
            })

        except Exception as e:
            print("Error creating user:", e)
            traceback.print_exc()  # This will give you a detailed error traceback in the console
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

        
@csrf_exempt
@login_required
@require_POST
def delete_user_view(request):
    try:
        data = json.loads(request.body)
        user_ids = data.get('user_ids', [])

        deleted_users = []

        for user_id in user_ids:
            try:
                user = CustomUser.objects.get(id=user_id)
                # Directly delete the user
                user.delete()
                deleted_users.append(user_id)
            except User.DoesNotExist:
                # Skip users that do not exist
                continue
        return JsonResponse({'success': True, 'deleted_users': deleted_users})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data.'}, status=400)

def logout_view(request):
    logout(request)  # Ends the user session
    return redirect('login')