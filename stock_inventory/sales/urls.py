from django.urls import path
from . import views

urlpatterns = [
    path('', views.sales, name='sales'),
    path('sales/', views.sales_management, name='sales_management'),
    path('salesmanagement/', views.sales_management, name='sales_management'),
    path('sales_terminal/', views.sales_terminal, name='sales_terminal'),
    path('update_sales/<int:product_id>/', views.update_sales, name='update_sales'),
    path('update_quantities/', views.update_quantities, name='update_quantities')
]