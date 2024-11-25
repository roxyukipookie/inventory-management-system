import traceback
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.db.models import F, Sum 
from .models import Product, Notification
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.hashers import check_password
import logging
from accounts.models import UserProfile 
from accounts.models import CustomUser
import django_excel as excel
import pyexcel
import pandas as pd


from .models import Profile
from django.http import HttpResponseForbidden


@login_required
def dashboard_view(request):
    products = Product.objects.all()

    # Data for the chart
    product_names = [product.name for product in products]
    remaining_quantities = [product.quantity for product in products]
    sold_quantities = [product.sold_quantity for product in products]

    total_products = Product.objects.count()
    total_stock = Product.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity']
    low_stock_items = Product.objects.filter(quantity__lt=F('alert_threshold')).count()
    out_of_stock_items = Product.objects.filter(quantity=0).count()  
    top_products_sold = Product.objects.order_by('-sold_quantity')[:5]
    recently_added_products = Product.objects.order_by('-created_at')[:5]
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')

    # Fetch the logged-in user's profile picture (if it exists)
    profile_picture = None
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            profile_picture = profile.profile_picture.url if profile.profile_picture else None
        except Profile.DoesNotExist:
            profile_picture = None

    context = {
        'total_products': total_products,
        'total_stock': total_stock,
        'low_stock_items': low_stock_items,
        'out_of_stock_items': out_of_stock_items,
        'top_products_sold': top_products_sold,
        'recently_added_products': recently_added_products,
        'notifications': notifications,  
        'product_names': product_names,  
        'remaining_quantities': remaining_quantities,  
        'sold_quantities': sold_quantities,
        'profile_picture': profile_picture,
        'username': request.user.username,
    }
    return render(request, 'dashboard.html', context)

def get_notifications(request):
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:5]
    unread_count = Notification.objects.filter(is_read=False).count()  # Count unread notifications

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
        'unread_count': unread_count  # Return unread count
    }, safe=False)

def export_products(request):
    products = Product.objects.all().values(
        'name', 'quantity', 'price', 'sold_quantity', 'total_sales', 'mfg_date', 'exp_date', 'description'
    )
    df = pd.DataFrame(list(products))

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
    df.to_excel(response, index=False, engine='openpyxl')

    return response

@login_required
def role_management_view(request):
    return render(request, 'role_management.html')

@login_required
def user_management_view(request):
    # Fetch only users who are staff
    users = User.objects.filter(role='Staff')
    
    # Get the count of staff users
    user_count = users.count()

    return render(request, 'user_management.html', {
        'users': users,
        'user_count': user_count
    })

@login_required
def inventory_view(request):
    # Restrict to superuser
    if not request.user.is_owner:
        return HttpResponseForbidden("You do not have permission to access this page.")
    # Continue with the logic for displaying inventory
    return render(request, 'inventory.html')

@login_required
def history_view(request):
    # Restrict to superuser
    if not request.user.is_owner:
        return HttpResponseForbidden("You do not have permission to access this page.")
    # Continue with the logic for displaying history
    return render(request, 'history.html')

@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')  # New username field
        password = request.POST.get('password')
        role = request.POST.get('role', '').lower()
        profile_picture = request.FILES.get('profile_picture')  # Profile picture upload

        try:
            # Step 1: Create the new user
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.set_password(password)
            user.save()

            # Step 2: Create the UserProfile with the role and profile picture
            if not UserProfile.objects.filter(user=user).exists():
                profile = UserProfile.objects.create(
                    user=user,
                    profile_picture=profile_picture  # Save profile picture
                )

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

                user.save()  # Save updated permissions
                profile.save()  # Save profile with role and picture

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
            # Print exact error for debugging
            print("Error creating user:", e)
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': 'Error creating user. Please check server logs for details.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


        
@csrf_exempt
def delete_users(request):
    if request.method == 'POST':
        try:
            user_ids = request.POST.getlist('user_ids')
            User.objects.filter(id__in=user_ids).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

"""User = get_user_model()
logger = logging.getLogger(__name__)

@csrf_exempt  # Consider using CSRF token handling in production
def reset_password_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.debug(f"Received data: {data}")  # Log the raw data received
            user_id = data.get('user_id')
            old_password = data.get('old_password')
            new_password = data.get('new_password')

            user = User.objects.get(id=user_id)
            logger.debug(f"Attempting to check password for user: {user.username}")

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                logger.debug("Password has been successfully changed.")
                return JsonResponse({'success': True, 'message': 'Password reset successfully.'})
            else:
                logger.debug("Old password is incorrect.")
                return JsonResponse({'success': False, 'message': 'Old password is incorrect.'})
        except User.DoesNotExist:
            logger.error("User not found.")
            return JsonResponse({'success': False, 'message': 'User not found.'})
        except json.JSONDecodeError:
            logger.error("Invalid JSON.")
            return JsonResponse({'success': False, 'message': 'Invalid JSON.'})
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})"""

User = get_user_model()

"""@csrf_exempt
def edit_role_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            new_role = data.get('role')  # Expecting 'staff' or 'owner'

            # Retrieve the user and verify existence
            user = User.objects.get(id=user_id)
            #profile = user.profile  # Access the related UserProfile instance
            profile, created = UserProfile.objects.get_or_create(user=user)

            
            # Update the role in UserProfile
            profile.role = new_role
            profile.save()  # Save the profile changes
            
            # Check if the role was saved correctly
            updated_profile = UserProfile.objects.get(user=user)
            print("Updated role:", updated_profile.role)  # Debugging statement

            return JsonResponse({
                'success': True,
                'role': updated_profile.role
            })

        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})"""

# views.py
@csrf_exempt
def edit_role_view(request):
    if request.method == 'POST':
        # Extract user_id and role from the request body
        data = json.loads(request.body)
        print(data)
        user_id = int(data.get('user_id'))
        new_role = data.get('role')
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found."}, status=400)

        # Update the role of the user
        if new_role == 'owner':
            user.is_superuser = True
            user.is_staff = True
        elif new_role == 'staff':
            user.is_superuser = False
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
        
        user.save()

        # Return the updated role information
        return JsonResponse({"success": True, "role": new_role})

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

def custom_logout_view(request):
    logout(request)
    return redirect('login')



