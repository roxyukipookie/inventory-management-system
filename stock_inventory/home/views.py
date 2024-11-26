from django.shortcuts import render
from dashboard.models import Product

# Create your views here.
def profile_view(request):
    product_count = Product.objects.count()

    context = {
        'product_count': product_count,
    }
    return render(request, 'profile.html', context)