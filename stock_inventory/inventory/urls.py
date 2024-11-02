from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory, name='inventory'),
    path('invoice/', views.invoice, name='invoice'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/', views.update_product, name='update_product'),
    path('history/', views.history, name='history'),
]