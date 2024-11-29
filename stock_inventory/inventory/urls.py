from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory, name='inventory'),
    path('add_category/', views.add_category, name='add_category'),
    path('delete_product/<str:barcode>/', views.delete_product, name='delete_product'),
    path('edit_product/<str:barcode>/', views.edit_product, name='edit_product'),
    path('history/', views.history, name='history'),
]