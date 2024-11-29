from django.shortcuts import render
from dashboard.models import Product

def history(request):
    print(Product.objects.all())
    products = Product.objects.all()
    print(products)

    recently_added_products = Product.objects.order_by('-created_at')

    context = {
        'recently_added_products' : recently_added_products

    }
    
    return render(request, 'history.html', context)
