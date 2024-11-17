from django.shortcuts import render, redirect,  get_object_or_404
from pages.models import Product, Category
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

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