from django.urls import path
from . import views

urlpatterns = [
    path('sales_terminal/', views.sales_terminal, name='sales_terminal')
]