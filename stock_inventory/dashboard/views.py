from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import F, Sum 
from .models import Product, Notification

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
        'sold_quantities': sold_quantities  
    }
    return render(request, 'dashboard.html', context)

def get_notifications(request):
    # Fetch unread notifications (you can filter them based on stock levels or other criteria)
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:5]  # Limit to 5 recent notifications

    # Prepare the notifications data in a list
    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'title': notification.title,
            'message': notification.message,
            'icon': notification.icon,  # Optional: add icon URL if needed
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'notification_type': notification.notification_type
        })

    # Return the data as a JSON response
    return JsonResponse(notifications_data, safe=False)

