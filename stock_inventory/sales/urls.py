from django.urls import path
from . import views

urlpatterns = [
    path('sales_terminal/', views.sales_terminal, name='sales_terminal'),
    path('add_to_sales_terminal/', views.add_to_sales_terminal, name='add_to_sales_terminal'),
    path('clear_sales_terminal/', views.clear_sales_terminal, name='clear_sales_terminal'),
    path('process_total/', views.process_total, name="process_total"),
]